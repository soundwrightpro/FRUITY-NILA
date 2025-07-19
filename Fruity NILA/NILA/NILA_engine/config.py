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

- `mixer_increment`: Controls the knob increment for mixer volume and pan.
    - This sets how much the mixer volume or pan changes with each knob turn.
    - Choose a value between 0.001 (0.1%) and 1.00 (100%).
    - Default is 0.005.

- `channel_increment`: Controls the knob increment for channel rack volume and pan.
    - Channel volume and pan are more sensitive, so avoid very small values.
    - Choose a value between 0.005 and 1.00.
    - Default is 0.01.

Note: Users can modify these settings to tailor the script behavior according to their preferences.
"""

# Configuration Settings
jog_preview_sound = 0
upDown_preview_sound = 1
rectChannel = 2000
rectMixer = 2000
mixer_increment = 0.002
channel_increment = 0.005
double_click_speed = 0.500 #ms
