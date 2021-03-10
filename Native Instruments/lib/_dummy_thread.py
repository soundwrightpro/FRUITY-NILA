# Copyright © 2001-2021 Python Software Foundation; All Rights Reserved

# PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
# --------------------------------------------

# 1. This LICENSE AGREEMENT is between the Python Software Foundation
# ("PSF"), and the Individual or Organization ("Licensee") accessing and
# otherwise using this software ("Python") in source or binary form and
# its associated documentation.

# 2. Subject to the terms and conditions of this License Agreement, PSF hereby
# grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
# analyze, test, perform and/or display publicly, prepare derivative works,
# distribute, and otherwise use Python alone or in any derivative version,
# provided, however, that PSF's License Agreement and PSF's notice of copyright,
# i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
# 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021 Python Software Foundation;
# All Rights Reserved" are retained in Python alone or in any derivative version
# prepared by Licensee.

# 3. In the event Licensee prepares a derivative work that is based on
# or incorporates Python or any part thereof, and wants to make
# the derivative work available to others as provided herein, then
# Licensee hereby agrees to include in any such work a brief summary of
# the changes made to Python.

# 4. PSF is making Python available to Licensee on an "AS IS"
# basis.  PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
# IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
# DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
# FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
# INFRINGE ANY THIRD PARTY RIGHTS.

# 5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
# FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
# A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
# OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

# 6. This License Agreement will automatically terminate upon a material
# breach of its terms and conditions.

# 7. Nothing in this License Agreement shall be deemed to create any
# relationship of agency, partnership, or joint venture between PSF and
# Licensee.  This License Agreement does not grant permission to use PSF
# trademarks or trade name in a trademark sense to endorse or promote
# products or services of Licensee, or any third party.

# 8. By copying, installing or otherwise using Python, Licensee
# agrees to be bound by the terms and conditions of this License
# Agreement.


"""Drop-in replacement for the thread module.

Meant to be used as a brain-dead substitute so that threaded code does
not need to be rewritten for when the thread module is not present.

Suggested usage is::

    try:
        import _thread
    except ImportError:
        import _dummy_thread as _thread

"""
# Exports only things specified by thread documentation;
# skipping obsolete synonyms allocate(), start_new(), exit_thread().
__all__ = ['error', 'start_new_thread', 'exit', 'get_ident', 'allocate_lock',
           'interrupt_main', 'LockType']

# A dummy value
TIMEOUT_MAX = 2**31

# NOTE: this module can be imported early in the extension building process,
# and so top level imports of other modules should be avoided.  Instead, all
# imports are done when needed on a function-by-function basis.  Since threads
# are disabled, the import lock should not be an issue anyway (??).

error = RuntimeError

def start_new_thread(function, args, kwargs={}):
    """Dummy implementation of _thread.start_new_thread().

    Compatibility is maintained by making sure that ``args`` is a
    tuple and ``kwargs`` is a dictionary.  If an exception is raised
    and it is SystemExit (which can be done by _thread.exit()) it is
    caught and nothing is done; all other exceptions are printed out
    by using traceback.print_exc().

    If the executed function calls interrupt_main the KeyboardInterrupt will be
    raised when the function returns.

    """
    if type(args) != type(tuple()):
        raise TypeError("2nd arg must be a tuple")
    if type(kwargs) != type(dict()):
        raise TypeError("3rd arg must be a dict")
    global _main
    _main = False
    try:
        function(*args, **kwargs)
    except SystemExit:
        pass
    except:
        import traceback
        traceback.print_exc()
    _main = True
    global _interrupt
    if _interrupt:
        _interrupt = False
        raise KeyboardInterrupt

def exit():
    """Dummy implementation of _thread.exit()."""
    raise SystemExit

def get_ident():
    """Dummy implementation of _thread.get_ident().

    Since this module should only be used when _threadmodule is not
    available, it is safe to assume that the current process is the
    only thread.  Thus a constant can be safely returned.
    """
    return -1

def allocate_lock():
    """Dummy implementation of _thread.allocate_lock()."""
    return LockType()

def stack_size(size=None):
    """Dummy implementation of _thread.stack_size()."""
    if size is not None:
        raise error("setting thread stack size not supported")
    return 0

def _set_sentinel():
    """Dummy implementation of _thread._set_sentinel()."""
    return LockType()

class LockType(object):
    """Class implementing dummy implementation of _thread.LockType.

    Compatibility is maintained by maintaining self.locked_status
    which is a boolean that stores the state of the lock.  Pickling of
    the lock, though, should not be done since if the _thread module is
    then used with an unpickled ``lock()`` from here problems could
    occur from this class not having atomic methods.

    """

    def __init__(self):
        self.locked_status = False

    def acquire(self, waitflag=None, timeout=-1):
        """Dummy implementation of acquire().

        For blocking calls, self.locked_status is automatically set to
        True and returned appropriately based on value of
        ``waitflag``.  If it is non-blocking, then the value is
        actually checked and not set if it is already acquired.  This
        is all done so that threading.Condition's assert statements
        aren't triggered and throw a little fit.

        """
        if waitflag is None or waitflag:
            self.locked_status = True
            return True
        else:
            if not self.locked_status:
                self.locked_status = True
                return True
            else:
                if timeout > 0:
                    import time
                    time.sleep(timeout)
                return False

    __enter__ = acquire

    def __exit__(self, typ, val, tb):
        self.release()

    def release(self):
        """Release the dummy lock."""
        # XXX Perhaps shouldn't actually bother to test?  Could lead
        #     to problems for complex, threaded code.
        if not self.locked_status:
            raise error
        self.locked_status = False
        return True

    def locked(self):
        return self.locked_status

    def __repr__(self):
        return "<%s %s.%s object at %s>" % (
            "locked" if self.locked_status else "unlocked",
            self.__class__.__module__,
            self.__class__.__qualname__,
            hex(id(self))
        )

# Used to signal that interrupt_main was called in a "thread"
_interrupt = False
# True when not executing in a "thread"
_main = True

def interrupt_main():
    """Set _interrupt flag to True to have start_new_thread raise
    KeyboardInterrupt upon exiting."""
    if _main:
        raise KeyboardInterrupt
    else:
        global _interrupt
        _interrupt = True