import device

def detectDevice(NILA_Name):
    """
    Gets the MIDI device name from FL Studio and sets `DEVICE_SERIES` to the right value for the script to work properly.

    Parameters:
    - NILA_Name (str): The name of the detected device series.

    Returns:
    - str: The updated NILA_Name based on the detected MIDI device.
    """

    # Get the current MIDI device name from FL Studio
    deviceName = device.getName()

    # Map FL Studio MIDI device names to corresponding NATIVE INSTRUMENTS device series names
    device_mapping = {
        "Komplete Kontrol A DAW": "Komplete Kontrol Series A",
        "Komplete Kontrol M DAW": "Komplete Kontrol Series M",
        "Komplete Kontrol DAW - 1": "Komplete Kontrol Series S",
        "KOMPLETE KONTROL M32": "Komplete Kontrol Series M",
        "KOMPLETE KONTROL M32 MIDI": "Komplete Kontrol Series M",
        "KOMPLETE KONTROL S88 MK2 Port 1": "Komplete Kontrol Series S",
        "KOMPLETE KONTROL - 1": "Komplete Kontrol Series S",
    }

    # Update NILA_Name based on the detected MIDI device
    NILA_Name = device_mapping.get(deviceName, device.getName())

    return NILA_Name

