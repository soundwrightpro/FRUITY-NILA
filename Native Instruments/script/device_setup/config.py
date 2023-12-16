"""
Start of User-editable Python file to change script behavior
"""

# Behavior of Browser Jog Wheel
# 
# If set to 0, sounds playing while jogging (spinning the rightmost knob) will be turned off.
# If set to 1, sounds will be turned on while jogging.

# Default is 0
jog_preview_sound = 0

# Behavior of Up/Down Jog Wheel
# 
# If set to 0, sounds playing while jogging (spinning the rightmost knob) will be turned off.
# If set to 1, sounds will be turned on while jogging.

# Default is 1
upDown_preview_sound = 1

# Behavior of Rectangle in Channel Rack & Mixer
# 
# If set to 0, the red rectangle won't be displayed when jogging (spinning the rightmost knob).
# If set to 2000, the red rectangle will be displayed for 2000 milliseconds (2 seconds).
# rectChannel controls the red rectangle for the Channel Rack, and rectMixer controls the red rectangle for the mixer.

# Default is 2000
rectChannel = 2000
rectMixer = 2000

# Knob increments
# This value sets the amount of increments for each message your keyboard sends to FL Studio
# when twisting the knobs on your device to change track volume and pan on the mixer. Choose a value between
# 0.01 (1%) and 1.00 (100%).

# Default is 0.01
increment = 0.01

"""
End of User-editable Python file to change script behavior
"""
