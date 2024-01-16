from script.device_setup import NILA_detect_device
from script.device_setup import constants

from sys import flags, platform
import device
import general
import ui

# Get FL Studio version information
VER_Major, VER_Minor, VER_Release = ui.getVersion(0), ui.getVersion(1), ui.getVersion(2)

def VersionCheck(compatibility):
    """
    Called to check the user's FL Studio version to see if this script can run.

    Parameters:
    - compatibility (bool): Indicates whether the script is compatible with the FL Studio version.

    Returns:
    - bool: Updated compatibility status.
    """

    # Initialize variables
    NILA_Name = ""
    OS = ""

    # Print output message from constants module
    print(constants.OUTPUT_MESSAGE)

    # Determine the operating system
    OS = "macOS" if platform == "darwin" else "Windows"

    # Check if FL Studio version is within the specified range
    if constants.MIN_Major <= int(VER_Major):
        if constants.MAX_Major == int(constants.MAX_Major):
            # Check compatibility based on minor version and MIDI script version
            if int(VER_Minor) >= constants.MAX_Minor and general.getVersion() >= constants.MIDI_Script_Version:
                print(f"{ui.getProgTitle()} {ui.getVersion()} is compatible with this script on {OS}\n")
                compatibility = True
            elif constants.MIN_Minor <= int(VER_Minor) >= constants.MIDI_Script_Version:
                print(f"{ui.getProgTitle()} {ui.getVersion()} is compatible with this script on {OS}\n")
                compatibility = True
        else:
            # Print compatibility error message if not within the specified range
            print(f"{ui.getProgTitle()} {ui.getVersion()} is not compatible with this script on {OS}\n\nFRUITY NILA {constants.VERSION_NUMBER} will not load on this device. \nPlease update {VER_Major} {ui.getVersion()} to {constants.MIN_Major}.{constants.MIN_Minor}.{constants.MIN_Release} or higher.\n")
            compatibility = False

    # Detect the series of the connected device
    seriesDevice = NILA_detect_device.detectDevice(NILA_Name)

    # Define a list of compatible series
    compatible_series = ['Komplete Kontrol Series A', 'Komplete Kontrol Series M', 'Komplete Kontrol Series S']

    # Check if the detected series is in the list of compatible series
    if seriesDevice in compatible_series:
        print(f"A {seriesDevice} has been detected. It is compatible with this script\n\n")
        compatibility = True
    else:
        # Print compatibility error message if the series is not compatible
        print(f"The {seriesDevice} is not compatible with this script. Only the {', '.join(compatible_series)} are compatible with FRUITY NILA\n\n")
        compatibility = False
        

    return compatibility