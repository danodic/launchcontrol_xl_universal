# Stores the current window
current_window = 'mixer'

# Stores the current mode
current_mode = 'mute'

# Store the status of the switches
mute_status = [None]*8
solo_status = [True]*8
arm_status = [None]*8

# Channel focus status
channel_focus = ['green_low'] * 8

# Store state of knobs
knob_status = [0]*8

# Status of the knobs
knob_mode = 'pan'

# Transport status
play_status = False
stop_status = False
rec_status = False

knob_leds = 0