from script.NILA_engine import NILA_detect_device
from script.NILA_engine import constants as c

from sys import platform
import device
import general
import ui

# Get FL Studio version information
VER_Major = ui.getVersion(0)
VER_Minor = ui.getVersion(1)
VER_Release = ui.getVersion(2)

def VersionCheck(compatibility):
	"""
	Called to check the user's FL Studio version and connected device compatibility.

	Parameters:
	- compatibility (bool): Indicates whether the script is compatible with the FL Studio version.

	Returns:
	- bool: Updated compatibility status.
	"""

	NILA_Name = ""
	OS = "macOS" if platform == "darwin" else "Windows"

	# Print output message from constants module (optional)
	print("-" * 75)
	print(c.OUTPUT_MESSAGE, c.GOODBYE_MESSAGE, "\n")

	# Version tuple comparisons
	current_version = (int(VER_Major), int(VER_Minor), int(VER_Release))
	min_version = (c.MIN_Major, c.MIN_Minor, c.MIN_Release)
	max_version = (c.MAX_Major, c.MAX_Minor, c.MAX_Release)

	# Check FL version range and MIDI scripting version
	DAW_compatible = min_version <= current_version <= max_version and general.getVersion() >= c.MIDI_Script_Version

	# Detect the series of the connected device
	seriesDevice = NILA_detect_device.detectDevice(NILA_Name)
	compatible_series = ['Komplete Kontrol Series A', 'Komplete Kontrol Series M', 'Komplete Kontrol Series S']
	Device_compatible = seriesDevice in compatible_series

	# Combined compatibility output
	if DAW_compatible and Device_compatible:
		print(f"{ui.getProgTitle()} {ui.getVersion()} on ({OS}) and {seriesDevice} detected, both are compatible with this script.\n")
		print("Need help or want to join the community? Join our Discord Fruity NI:", c.DISCORD)
		print("\nReady for use with FL Studio.\n")
		compatibility = True
	elif not DAW_compatible:
		print(f"{ui.getProgTitle()} {ui.getVersion()} is not compatible with this script on {OS}\n\nFRUITY NILA {c.VERSION_NUMBER} will not load on this device.\nPlease update to {c.MIN_Major}.{c.MIN_Minor}.{c.MIN_Release} or higher.\n")
		print("Need help or want to join the community? Join our Discord Fruity NI:", c.DISCORD)
		print("\nNot ready for use with FL Studio.\n")
		compatibility = False
	elif not Device_compatible:
		print(f"The {seriesDevice} is not compatible with this script. Only the {', '.join(compatible_series)} are supported by FRUITY NILA.")
		print("Need help or want to join the community? Join our Discord Fruity NI:", c.DISCORD)
		print("\nNot ready for use with FL Studio.\n")
		compatibility = False

	print("-" * 75)
	return compatibility
