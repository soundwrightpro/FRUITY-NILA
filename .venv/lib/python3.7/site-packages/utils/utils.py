"""Utilities Module (included in FL Studio Python lib folder)

Contains useful functions and classes for use when working with FL Studio's
Python API

NOTE: This code is taken from FL Studio's Python lib folder and included in this
package in the hope that it will be useful for script developers. It is not the
creation of the repository authors, and no credit is claimed for the code
content.

However, the documentation for the provided code is created by the
authors of this repository.

WARNING: Some of the provided functions in the FL Studio installation have bugs
that may result in unexpected behaviour. These bugs have been left as-is in this
file for your inspection and warnings have been added to the docstrings. Use
these functions with caution.
"""

import math

class TRect:
    """Represents a rectangle object
    """
    def __init__(self, left: int, top: int, right: int, bottom: int):
        """Create a `TRect` object representing a rectangle

        Args:
         * left (int): left position
         * top (int): top position
         * right (int): right position
         * bottom (int): bottom position
        """
        self.Top = top
        self.Left = left
        self.Bottom = bottom
        self.Right = right

    def Width(self) -> int:
        """Returns width of a rectangle

        Returns:
         * int: width
        """
        return self.Right - self.Left

    def Height(self) -> int:
        """Returns the height of a rectangle

        Returns:
         * int: height
        """
        return self.Bottom - self.Top

class TClipLauncherLastClip:
    def __init__(self, trackNum, subNum, flags):
        self.TrackNum = trackNum
        self.SubNum = subNum
        self.Flags = flags

def RectOverlapEqual(R1: TRect, R2: TRect) -> bool:
    """Returns whether two rectangles are overlapping or touching

    Args:
     * R1 (TRect): rectangle 1
     * R2 (TRect): rectangle 2

    Returns:
     * bool: whether rectangles overlap or touch
    """
    return (R1.Left <= R2.Right) & (R1.Right >= R2.Left) & (R1.Top <= R2.Bottom) & (R1.Bottom >= R2.Top)

def RectOverlap(R1: TRect, R2: TRect) -> bool:
    """Returns whether two rectangles are overlapping

    Args:
     * R1 (TRect): rectangle 1
     * R2 (TRect): rectangle 2

    Returns:
     * bool: whether rectangles overlap
    """
    return  (R1.Left < R2.Right) & (R1.Right > R2.Left) & (R1.Top < R2.Bottom) & (R1.Bottom > R2.Top)

def Limited(Value: float, Min: float, Max: float) -> float:
    """Limit a value to within the range `Min` - `Max`

    Args:
     * Value (float): Current value
     * Min (float): Min value
     * Max (float): Max value

    Returns:
     * float: limited value
    """
    if Value <= Min:
        res = Min
    else:
        res = Value
    if res > Max:
        res = Max
    return res

def InterNoSwap(X, A, B) -> bool:
    """Returns whether A <= X <= B, ie. whether X lies between A and B

    Args:
     * X (number): x
     * A (number): a
     * B (number): b

    Returns:
     * bool
    """
    return (X >= A) & (X <= B)

def DivModU(A: int, B: int) -> 'tuple[int, int]':
    """Return integer division and modulus

    Args:
     * A (int): int 1
     * B (int): int 2

    Returns:
     * int: integer division
     * int: modulus
    """
    C = A % B
    return (A // B), C

def SwapInt(A, B):
    """Given A and B, return B and A

    It's probably easier to just manually write
    ```py
    A, B = B, A
    ```
    in your code to begin with.

    Args:
     * A (any): thing 1
     * B (any): thing 2

    Returns:
     * tuple: B, A
    """
    return B, A

def Zeros(value, nChars, c = '0'):
    """TODO

    Args:
     * value ([type]): [description]
     * nChars ([type]): [description]
     * c (str, optional): [description]. Defaults to '0'.

    Returns:
     * [type]: [description]
    """
    if value < 0:
        Result = str(-value)
        Result = '-' + c * (nChars - len(Result)) + Result
    else:
        Result = str(value)
        Result = c * (nChars - len(Result)) + Result
    return Result

def Zeros_Strict(value, nChars, c ='0'):
    """TODO

    Args:
     * value ([type]): [description]
     * nChars ([type]): [description]
     * c (str, optional): [description]. Defaults to '0'.

    Returns:
     * [type]: [description]
    
    WARNING:
     * Strict trimming looks incorrect
    """
    if value < 0:
        Result = str(-value)
        Result = '-' +  c * (nChars - len(Result) - 1) + Result
    else:
        Result = str(value)
        Result = c * (nChars - len(Result)) + Result
    if len(Result) > nChars:
        Result = Result[len(Result) - nChars]
    return Result

def Sign(value: 'float | int') -> int:
    """Equivalent to `SignOf()`

    Args:
     * value (float | int): number

    Returns:
     * int: sign
    """
    if value < 0: 
        return -1
    elif value == 0:
        return 0
    else:   
        return 1

SignBitPos_64 = 63
SignBit_64 = 1 << SignBitPos_64
SignBitPos_Nat = SignBitPos_64

def SignOf(value: 'float | int') -> int:
    """Return the sign of a numerical value

    Args:
     * value (float | int): number

    Returns:
     * int: sign:
            * `0`: zero
            * `1`: positive
            * `-1`: negative
    """
    if value == 0:
        return 0
    elif value < 0:
        return -1
    else:   
        return 1

def KnobAccelToRes2(Value):
    """TODO

    Args:
     * Value ([type]): [description]

    Returns:
     * [type]: [description]
    """
    n = abs(Value)
    if n > 1:
        res = n ** 0.75
    else:
        res = 1
    return res

def OffsetRect(R: TRect, dx: int, dy: int) -> None:
    """Offset a rectangle by `dx` and `dy`

    Args:
     * R (TRect): rectangle
     * dx (int): x offset
     * dy (int): y offset
    
    NOTE: Rectangle is adjusted in-place
    """
    R.Left = R.Left + dx
    R.Top = R.Top + dy
    R.Right = R.Right + dx
    R.Bottom = R.Bottom + dy

def RGBToHSV(R: float, G: float, B: float) -> 'tuple[float, float, float]':
    """Convert an RGB colour to a HSV colour

    TODO: What scale is being used? 0.0-1.0 or 0-255?

    Args:
     * R (float): red
     * G (float): green
     * B (float): blue

    Returns:
     * H: hue
     * S: saturation
     * V: value (brightness)
    """
    Min = min(min(R, G), B)
    V = max(max(R, G), B)

    Delta = V - Min

    if V == 0:
        S = 0
    else:
        S = Delta / V

    if S == 0.0:
        H = 0.0 
    else:
        if R == V:
            H = 60.0 * (G - B) / Delta
        elif G == V:
            H = 120.0 + 60.0 * (B - R) / Delta
        elif B == V:
            H = 240.0 + 60.0 * (R - G) / Delta

        if H < 0.0:
            H = H + 360.0

    return H, S, V

def RGBToHSVColor(Color: int) -> 'tuple[float, float, float]':
    """Convert an RGB colour to a HSV colour

    Args:
     * Color (int): colour as integer (`0x--RRGGBB`)

    Returns:
     * H: hue
     * S: saturation
     * V: value (brightness)
    """
    r = ((Color & 0xFF0000) >> 16) / 255
    g = ((Color & 0x00FF00) >> 8) / 255
    b = ((Color & 0x0000FF) >> 0) / 255
    H, S, V = RGBToHSV(r, g, b)
    return H, S, V

def HSVtoRGB(H: float, S: float, V: float) -> 'tuple[float, float, float]':
    """Convert an HSV colour to an RGB colour

    Args:
     * H (float): hue
     * S (float): saturation
     * V (float): value (brightness)

    Returns:
     * float: red
     * float: green
     * float: blue
    """
    hTemp = 0
    if S == 0.0:
        R = V
        G = V
        B = V
    else:
        if H == 360.0:
            hTemp = 0.0
        else:
            hTemp = H

        hTemp = hTemp / 60
        i = math.trunc(hTemp)
        f = hTemp - i

        p = V * (1.0 - S)
        q = V * (1.0 - (S * f))
        t = V * (1.0 - (S * (1.0 - f)))

        if i == 0:
            R = V
            G = t
            B = p
        elif i == 1:
            R = q
            G = V
            B = p
        elif i == 2:
            R = p
            G = V
            B = t
        elif i == 3:
            R = p
            G = q
            B = V
        elif i == 4:
            R = t
            G = p
            B = V
        elif i == 5:
            R = V
            G = p
            B = q
    return R, G, B

NoteNameT = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

def GetNoteName(NoteNum: int) -> str:
    """Return the note name given a note number

    Args:
     * NoteNum (int): note number

    Returns:
     * str: note name
    """
    NoteNum += 1200
    return NoteNameT[NoteNum % 12] + str((NoteNum // 12) - 100)

def ColorToRGB(Color: int) -> 'tuple[int, int, int]':
    """Convert an integer colour to an RGB tuple that uses range 0-255.

    Args:
     * Color (int): colour as integer

    Returns:
     * int: red
     * int: green
     * int: blue
    """
    return (Color >> 16) & 0xFF, (Color >> 8) & 0xFF, Color & 0xFF

def RGBToColor(R: int, G: int, B: int) -> int:
    """convert an RGB set to an integer colour. values must be 0-255

    Args:
     * R (int): red
     * G (int): green
     * B (int): blue

    Returns:
     * int: colour
    """
    return (R << 16) | (G << 8) | B

def FadeColor(StartColor: int, EndColor: int, Value: float) -> int:
    """Fade between two colour values

    Args:
     * StartColor (int): colour integer
     * EndColor (int): colour integer
     * Value (float): fade position (0-255)

    Returns:
     * int: faded colour
    
    WARNING:
     * Blue value is incorrect, using green start value
    """
    rStart, gStart, bStart = ColorToRGB(StartColor)
    rEnd, gEnd, bEnd = ColorToRGB(EndColor)
    ratio = Value / 255
    rEnd = round(rStart * (1 - ratio) + (rEnd * ratio))
    gEnd = round(gStart * (1 - ratio) + (gEnd * ratio))
    bEnd = round(gStart * (1 - ratio) + (bEnd * ratio))
    return RGBToColor(rEnd, gEnd, bEnd)

def LightenColor(Color: int, Value: float) -> int:
    """Lighten a colour by a certain amount

    Args:
     * Color (int): colour integer
     * Value (float): amount to lighten by (0-255)

    Returns:
     * int: lightened colour
    """
    r, g, b = ColorToRGB(Color)
    ratio = Value / 255
    return RGBToColor(round(r + (1.0 - r) * ratio), round(g + (1.0 - g) * ratio) , round(b + (1.0 - b) * ratio))

def VolTodB(Value: float) -> float:
    """Convert volume as a decimal (0.0 - 1.0) to a decibel value

    Args:
     * Value (float): volume

    Returns:
     * float: volume in decibels
    """
    Value = (math.exp(Value * math.log(11)) - 1) * 0.1
    if Value == 0:
        return 0
    return round(math.log10(Value) * 20, 1)
