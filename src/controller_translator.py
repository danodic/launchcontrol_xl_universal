import mido
import keyboard
import time

import controller_status as state

def move_fader(midiout, value, control):
    """
    Will convert the midi input to pitch wheel values and then send the proper thing as a control change.
    """

    # Convert to pithbend and get the proper fader from the control number (first fader will be control 77)
    value = convert_midi_to_pitchbend(value)
    actual_control = control-77

    # Send the message
    message =  mido.Message('pitchwheel', pitch = value, channel = actual_control)
    midiout.send(message)

def move_knob(midiout, value, control):
    """
    Will convert the midi input to pitch wheel values and then send the proper thing as a control change.
    """

    difference = value - state.knob_status[control-49]

    # Check the motion direction
    motion = 65 if (difference / abs(difference)) < 0 else 1

    # Store the status of the knob
    state.knob_status[control-49] = value

    # Convert to pithbend and get the proper fader from the control number (first fader will be control 77)
    actual_control = control-33

    # Send the message
    message =  mido.Message('control_change', control = actual_control, channel = 0, value = motion )
    midiout.send(message)

def bank_right(midiout):
    """
    Will send the note 47, that shifts the bank right
    """

    # Send the message
    message =  mido.Message('note_on', note=47, velocity = 127)
    midiout.send(message)

def bank_left(midiout):
    """
    Will send the note 46, that shifts the bank left
    """

    # Send the message
    message =  mido.Message('note_on', note=46, velocity = 127)
    midiout.send(message)

def mixer_channel_right(midiout):
    """
    Will move the selection to the previous channel.
    """

    # Send the message
    message =  mido.Message('note_on', note=49, velocity = 127)
    midiout.send(message)

def mixer_channel_left(midiout):
    """
    Will move the selection to the next channel.
    """

    # Send the message
    message =  mido.Message('note_on', note=48, velocity = 127)
    midiout.send(message)

def channel_up(midiout):
    """

    """

    activate_pattern_window(midiout)

    # Send the message
    messages =  [
        mido.Message('note_on', note=96, velocity = 127),
        mido.Message('note_off', note=96, velocity = 0)
    ]
    
    # Send the messages
    for message in messages:
        midiout.send(message)

def channel_down(midiout):
    """

    """

    activate_pattern_window(midiout)

    # Send the message
    messages =  [
        mido.Message('note_on', note=97, velocity = 127),
        mido.Message('note_off', note=97, velocity = 0)
    ]
    
    # Send the messages
    for message in messages:
        midiout.send(message)

def move_channel_up(midiout):
    """

    """

    activate_pattern_window(midiout)

    keyboard.send('alt', True, False)
    keyboard.send('up', True, False)
    keyboard.send('up', False, True)
    keyboard.send('alt', False, True)

def move_channel_down(midiout):
    """

    """

    activate_pattern_window(midiout)

    keyboard.send('alt', True, False)
    keyboard.send('down', True, False)
    keyboard.send('down', False, True)
    keyboard.send('alt', False, True)

def mute(midiout, note):
    """

    """

    # Map notes to keys
    buttons = {
        73: 16,
        74: 17,
        75: 18,
        76: 19,
        89: 20,
        90: 21,
        91: 22,
        92: 23,
    }

    # Send the message
    message =  mido.Message('note_on', note=buttons[note], velocity = 127)
    midiout.send(message)

    message =  mido.Message('note_on', note=buttons[note], velocity = 0)
    midiout.send(message)

def solo(midiout, note):
    """

    """

    # Map notes to keys
    buttons = {
        73: 8,
        74: 9,
        75: 10,
        76: 11,
        89: 12,
        90: 13,
        91: 14,
        92: 15,
    }

    # Send the message
    message =  mido.Message('note_on', note=buttons[note], velocity = 127)
    midiout.send(message)

    message =  mido.Message('note_on', note=buttons[note], velocity = 0)
    midiout.send(message)

def record_arm(midiout, note):
    """

    """

    # Map notes to keys
    buttons = {
        73: 0,
        74: 1,
        75: 2,
        76: 3,
        89: 4,
        90: 5,
        91: 6,
        92: 7,
    }

    # Send the message
    message =  mido.Message('note_on', note=buttons[note], velocity = 127)
    midiout.send(message)

    message =  mido.Message('note_on', note=buttons[note], velocity = 0)
    midiout.send(message)


def convert_midi_to_pitchbend(midi):
    """
    Will convert 0-127 to -8192 - 8191.
    """

    if(midi >= 63):
        return int( (8191/63)*(midi-64) )
    else:
        return int( (8192/64)*(64-midi) ) * -1


def activate_pattern_window(midiout):
    messages =  [
        mido.Message('note_on', note=75, velocity = 127),
        mido.Message('note_off', note=75, velocity = 0),
    ]

    # Send the messages
    for message in messages:
        midiout.send(message)

def activate_browser_window(midiout):
    messages =  [
        mido.Message('note_on', note=74, velocity = 127),
        mido.Message('note_off', note=74, velocity = 0),
    ]

    # Send the messages
    for message in messages:
        midiout.send(message)

def browser_up(midiout):

    # activate pattern
    activate_browser_window(midiout)

    time.sleep(0.1)

    keyboard.send('up', True, False)
    keyboard.send('up', False, True)

def browser_down(midiout):
    # activate pattern
    activate_browser_window(midiout)

    time.sleep(0.1)

    keyboard.send('down', True, False)
    keyboard.send('down', False, True)

def browser_left(midiout):
    # activate pattern
    activate_browser_window(midiout)

    time.sleep(0.1)

    keyboard.send('left', True, False)
    keyboard.send('left', False, True)

def browser_right(midiout):
    # activate pattern
    activate_browser_window(midiout)

    time.sleep(0.1)

    keyboard.send('right', True, False)
    keyboard.send('right', False, True)

def activate_channel(midiout, note):
    """
    
    """

    # Send the message
    message =  mido.Message('note_on', note=note+24, velocity = 127)
    midiout.send(message)

def cursor_up(midiout):
    # Send the message
    keyboard.send('up', True, False)
    keyboard.send('up', False, True)

def cursor_down(midiout):
    # Send the message
    keyboard.send('down', True, False)
    keyboard.send('down', False, True)

def cursor_left(midiout):
    # Send the message
    keyboard.send('left', True, False)
    keyboard.send('left', False, True)

def cursor_right(midiout):
    # Send the message
    keyboard.send('right', True, False)
    keyboard.send('right', False, True)

def stop(midiout):
    messages =  [
        mido.Message('note_on', note=93, velocity = 127),
        mido.Message('note_on', note=93, velocity = 0)
    ]

    # Send the messages
    for message in messages:
        midiout.send(message)

def play(midiout):

    messages =  [
        mido.Message('note_on', note=94, velocity = 127),
        mido.Message('note_on', note=94, velocity = 0)
    ]

    # Send the messages
    for message in messages:
        midiout.send(message)

def record(midiout):
    messages =  [
        mido.Message('note_on', note=95, velocity = 127),
        mido.Message('note_on', note=95, velocity = 0)
    ]

    # Send the messages
    for message in messages:
        midiout.send(message)

def rewind(midiout):
    message =  mido.Message('note_on', note=91, velocity = 127)
    midiout.send(message)

def rewind_off(midiout):
    message =  mido.Message('note_on', note=91, velocity = 0)
    midiout.send(message)

def forward(midiout):
    message =  mido.Message('note_on', note=92, velocity = 127)
    midiout.send(message)

def forward_off(midiout):
    message =  mido.Message('note_on', note=92, velocity = 0)
    midiout.send(message)

def enter(midiout):
    keyboard.send('enter', True, False)
    keyboard.send('enter', False, True)

def tab(midiout):
    keyboard.send('tab', True, False)
    keyboard.send('tab', False, True)

def pan(midiout):
    messages =  [
        mido.Message('note_on', note=40, velocity = 127),
        mido.Message('note_on', note=40, velocity = 0)
    ]

    # Send the messages
    for message in messages:
        midiout.send(message)

def stereo(midiout):
    messages =  [
        mido.Message('note_on', note=41, velocity = 127),
        mido.Message('note_on', note=41, velocity = 0)
    ]

    # Send the messages
    for message in messages:
        midiout.send(message)

def sends(midiout):
    messages =  [
        mido.Message('note_on', note=42, velocity = 127),
        mido.Message('note_on', note=42, velocity = 0)
    ]

    # Send the messages
    for message in messages:
        midiout.send(message)

def effect(midiout):
    messages =  [
        mido.Message('note_on', note=43, velocity = 127),
        mido.Message('note_on', note=43, velocity = 0)
    ]

    # Send the messages
    for message in messages:
        midiout.send(message)

def eq(midiout):
    messages =  [
        mido.Message('note_on', note=44, velocity = 127),
        mido.Message('note_on', note=45, velocity = 0)
    ]

    # Send the messages
    for message in messages:
        midiout.send(message)
