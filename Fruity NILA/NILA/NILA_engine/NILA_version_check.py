from sys import platform

import general
import ui

from NILA.NILA_engine import NILA_detect_device, constants as c


# Get FL Studio version information
VER_Major = ui.getVersion(0)
VER_Minor = ui.getVersion(1)
VER_Release = ui.getVersion(2)
SUPPORTED_SERIES = (
	"Komplete Kontrol Series A",
	"Komplete Kontrol Series M",
	"Komplete Kontrol Series S",
)



def _print_header():
	print("-" * 75)
	print(c.OUTPUT_MESSAGE, c.GOODBYE_MESSAGE, "\n")



def _print_footer():
	print("-" * 75)



def _print_support_message():
	print("Need help or want to join the community? Join our Discord Fruity NI:", c.DISCORD)



def _format_version(version_tuple):
	return ".".join(str(part) for part in version_tuple)



def VersionCheck(compatibility):
	"""
	Called to check the user's FL Studio version and connected device compatibility.

	Parameters:
	- compatibility (bool): Indicates whether the script is compatible with the FL Studio version.

	Returns:
	- bool: Updated compatibility status.
	"""

	OS = "macOS" if platform == "darwin" else "Windows"
	NILA_Name = ""
	current_version = (int(VER_Major), int(VER_Minor), int(VER_Release))
	min_version = (c.MIN_Major, c.MIN_Minor, c.MIN_Release)
	max_version = (c.MAX_Major, c.MAX_Minor, c.MAX_Release)
	current_midi_script_version = general.getVersion()

	DAW_compatible = min_version <= current_version <= max_version and current_midi_script_version >= c.MIDI_Script_Version
	seriesDevice = NILA_detect_device.detectDevice(NILA_Name)
	Device_compatible = seriesDevice in SUPPORTED_SERIES
	compatibility = DAW_compatible and Device_compatible

	_print_header()
	print(f"Script version: FRUITY NILA {c.VERSION_NUMBER}")
	print(f"Operating system: {OS}")
	print(f"Detected DAW: {ui.getProgTitle()} {ui.getVersion()}")
	print(f"Detected MIDI scripting version: {current_midi_script_version}")
	print(f"Required MIDI scripting version: {c.MIDI_Script_Version}")
	print(f"Supported FL Studio range: {_format_version(min_version)} to {_format_version(max_version)}")
	print(f"Detected device: {seriesDevice}")
	print(f"Supported devices: {', '.join(SUPPORTED_SERIES)}\n")

	if compatibility:
		print(f"{ui.getProgTitle()} {ui.getVersion()} on {OS} is compatible with FRUITY NILA.")
		print(f"{seriesDevice} is supported and ready to use with this script.\n")
		print("Status: Ready for use with FL Studio.\n")
	else:
		print("Status: Not ready for use with FL Studio.\n")

		if not DAW_compatible:
			print(f"FL Studio compatibility check failed for {ui.getProgTitle()} {ui.getVersion()} on {OS}.")
			print(f"Supported FL Studio versions: {_format_version(min_version)} to {_format_version(max_version)}")
			print(f"Required MIDI scripting version: {c.MIDI_Script_Version}")
			print(f"Detected MIDI scripting version: {current_midi_script_version}\n")

		if not Device_compatible:
			print(f"The detected device is not supported: {seriesDevice}")
			print(f"Supported devices: {', '.join(SUPPORTED_SERIES)}\n")

		print(f"FRUITY NILA {c.VERSION_NUMBER} will not load until the compatibility issues above are resolved.\n")

	_print_support_message()
	print()
	_print_footer()
	return compatibility