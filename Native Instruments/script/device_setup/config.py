"""
Configuration Settings for User-Editable Python Script

This section of the script allows users to customize the behavior of the script by modifying various settings.

- `jog_preview_sound`: Controls the behavior of the Browser Jog Wheel.
    - If set to 0, sounds playing while jogging (spinning the rightmost knob) will be turned off.
    - If set to 1, sounds will be turned on while jogging.
    - Default is 0.

- `upDown_preview_sound`: Controls the behavior of the Up/Down Jog Wheel.
    - If set to 0, sounds playing while jogging (spinning the rightmost knob) will be turned off.
    - If set to 1, sounds will be turned on while jogging.
    - Default is 1.

- `rectChannel` and `rectMixer`: Control the behavior of the red rectangle in the Channel Rack and Mixer, respectively.
    - If set to 0, the red rectangle won't be displayed when jogging (spinning the rightmost knob).
    - If set to a positive value, the red rectangle will be displayed for the specified duration in milliseconds.
    - Default is 2000 for both `rectChannel` and `rectMixer`.

- `increment`: Controls the knob increments.
    - This value sets the amount of increments for each message your keyboard sends to FL Studio
      when twisting the knobs on your device to change track volume and pan on the mixer.
    - Choose a value between 0.01 (1%) and 1.00 (100%).
    - Default is 0.01.

Note: Users can modify these settings to tailor the script behavior according to their preferences.

"""
# Configuration Settings
jog_preview_sound = 0
upDown_preview_sound = 1
rectChannel = 2000
rectMixer = 2000
increment = 0.01
