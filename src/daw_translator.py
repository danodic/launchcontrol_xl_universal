import mido
import controller_status as state

default_header = 'F0 00 20 29 02 11'
default_channel = '0B'

off = '0C'
red_low = '0D'
red_full = '0F'
amber_low = '1D'
amber_full = '3F'
yellow = '3E'
green_low = '1C'
green_full = '3C'

colors = {
    'off': off,
    None: off,
    'red': red_full,
    'red_low': red_low,
    'amber': amber_full,
    'amber_low': amber_low,
    'yellow': yellow,
    'yellow_low': amber_low,
    'green': green_full,
    'green_low': green_low
}

def light_on_track_focus(midiout, note):

    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, str(hex(note)).replace('0x', ''), green_full, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_off_track_focus(midiout, note):

    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, str(hex(note)).replace('0x', ''), green_low, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_on_mute(midiout, note):

    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, str(hex(note + 16)).replace('0x', ''), red_full, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_off_mute(midiout, note):
    
    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, str(hex(note + 16)).replace('0x', ''), green_full, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_on_device(midiout):

    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, '28', amber_full, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_off_device(midiout):
    
    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, '28', off, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_on_arm(midiout, note):

    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, str(hex(note + 32)).replace('0x', ''), red_full, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_off_arm(midiout, note):
    
    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, str(hex(note + 32)).replace('0x', ''), amber_low, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_on_mute_btn(midiout):
    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, '29', amber_full, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_off_mute_btn(midiout):
    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, '29', off, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_on_solo_btn(midiout):
    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, '2A', amber_full, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_off_solo_btn(midiout):
    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, '2A', off, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_on_arm_btn(midiout):
    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, '2B', amber_full, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def light_off_arm_btn(midiout):
    # Send the note
    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, '2B', off, 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)

def store_mute_solo_status(note, velocity):

    if velocity == 127:
        # Store the state
        state.mute_status[note-16] = True
        state.solo_status[note-16] = False

    else:
        # Store the state
        state.mute_status[note-16] = False
        state.solo_status[note-16] = True

def store_arm_status(note, velocity):

    if velocity == 127:
        # Store the state
        state.arm_status[note] = True

    else:
        # Store the state
        state.arm_status[note] = False

def light_on(midiout, note, color):

    message = '%s %s %s %s %s %s' % (default_header, '78', default_channel, str(hex(note)).replace('0x', ''), colors[color], 'F7')
    message = mido.Message.from_hex(message)
    midiout.send(message)
