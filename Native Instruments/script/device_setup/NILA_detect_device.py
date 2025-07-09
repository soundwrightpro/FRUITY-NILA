import device

DEVICE_MAPPING = {
	"komplete kontrol a daw": "Komplete Kontrol Series A",
	"komplete kontrol m daw": "Komplete Kontrol Series M",
	"komplete kontrol daw - 1": "Komplete Kontrol Series S",
	"komplete kontrol m32": "Komplete Kontrol Series M",
	"komplete kontrol m32 midi": "Komplete Kontrol Series M",
	"komplete kontrol s88 mk2 port 1": "Komplete Kontrol Series S",
	"komplete kontrol - 1": "Komplete Kontrol Series S",
}

DEFAULT_SERIES = "Unknown Komplete Kontrol Series"

def detect_device(NILA_Name=None) -> str:
	"""
	Detects the current MIDI device and returns the appropriate Komplete Kontrol series name.

	Args:
	    NILA_Name (optional): Ignored. Present for backward compatibility.

	Returns:
	    str: The detected Komplete Kontrol Series name (or fallback if unknown).
	"""
	device_name = device.getName().strip().lower()
	return DEVICE_MAPPING.get(device_name, DEFAULT_SERIES)

# Backward compatibility alias
detectDevice = detect_device