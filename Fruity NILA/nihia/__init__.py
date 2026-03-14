# MIT License

# Copyright (c) 2021 Pablo Peral

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Python package for the FL Studio MIDI API to take advantage of the MIDI mode of the Native Instruments Host
Integration Agent protocol and use the DAW integration mode of Komplete Kontrol keyboards.
"""

__all__ = ["buttons", "mixer"]

import device

SYSEX_HEADER = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0]

def dataOut(data1, data2):
	"""Send a normal MIDI message in the form BF data1 data2."""
	data1 = int(data1) & 0x7F
	data2 = int(data2) & 0x7F
	message = 0xBF | (data1 << 8) | (data2 << 16)

	if device.isAssigned():
		device.midiOutMsg(message)

def handShake():
	"""Wake the device from MIDI mode and activate deep integration."""
	dataOut(1, 3)

def goodBye():
	"""Exit deep integration mode before FL Studio closes."""
	dataOut(2, 1)