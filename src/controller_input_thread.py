import threading
import time
import mido
import pdb

import controller_translator as translator
import daw_translator as d_translator
import controller_status as state

class ControllerInputThread (threading.Thread):
    """

    """

    def __init__(self, midiin_launchcontrol=None, midiin_external=None, midiout_launchcontrol=None, midiout_external=None):
        """
        TODO
        """

        self.default_timeout = 0.0001

        # Initialize the threading lib
        threading.Thread.__init__(self)

        # Store some variables
        self.midiin_external = midiin_external
        self.midiin_launchcontrol = midiin_launchcontrol
        self.midiout_external = midiout_external
        self.midiout_launchcontrol = midiout_launchcontrol
        self.keep_running = True
        self.running = False

        # faders
        self.faders = [77, 78, 79, 80, 81, 82, 83, 84]
        self.bottom_buttons = [73, 74, 75, 76, 89, 90, 91, 92]
        self.knobs = [49, 50, 51, 52, 53, 54, 55, 56]
        self.top_buttons = [41, 42, 43, 44, 57, 58, 59, 60]

    def run(self):
        self.wait_for_midi_devices()

        if not self.keep_running:
            return

        self.running = True
        self.main()

    def wait_for_midi_devices(self):
        while (self.midiin_launchcontrol is None or self.midiin_external is None or self.midiout_external is None or self.midiout_launchcontrol is None) and self.keep_running:
            time.sleep(self.default_timeout)

    def main(self):
        """

        """

        self.restore_screen_state()

        while self.keep_running:

            # Get the message
            message = self.midiin_launchcontrol.poll()

            if message:

                # Organize the values
                data = message.dict()

                print("output", data)

                # Note
                if data['type'] in ['note_on', 'note_off']:
                    
                    # Device key (Shift)
                    if data['note'] == 105 and data['velocity'] == 127:
                        self.shift()
                        self.restore_screen_state()
                        self.light_off_device()

                    elif data['note'] in self.top_buttons and data['velocity'] == 127:
                        self.activate_channel(data['note'])

                    # Mute
                    elif data['note'] == 106 and data['velocity'] == 127:
                        state.current_mode = 'mute'
                        self.lower_panel()
                        self.light_right_panel()

                    # Solo
                    elif data['note'] == 107 and data['velocity'] == 127:
                        state.current_mode = 'solo'
                        self.lower_panel()
                        self.light_right_panel()

                    # Record Arm
                    elif data['note'] == 108 and data['velocity'] == 127:
                        state.current_mode = 'arm'
                        self.lower_panel()
                        self.light_right_panel()

                    # Solo/Mute/Record
                    elif data['note'] in self.bottom_buttons and data['velocity'] == 127:
                        
                        if state.current_mode == 'mute':
                            translator.mute(self.midiout_external, data['note'])

                        elif state.current_mode == 'solo':
                            translator.solo(self.midiout_external, data['note'])

                        elif state.current_mode == 'arm':
                            translator.record_arm(self.midiout_external, data['note'])

                # Control change
                elif data['type'] == 'control_change':

                    if data['control'] in self.faders:

                        # Send the fader movement
                        translator.move_fader(self.midiout_external, data['value'], data['control'])

                    elif data['control'] in self.knobs:
                            translator.move_knob(self.midiout_external, data['value'], data['control'])

                    # Check arrow keys
                    self.arrow_keys(data)                       

            time.sleep(self.default_timeout)

    def shift(self):

        # Light the panel
        self.light_right_panel_shift()
        self.light_on_device()
        self.lower_panel_shift()

        while self.keep_running:

            # Get the message
            message = self.midiin_launchcontrol.poll()

            if message:

                # Organize the values
                data = message.dict()

                print("output", data)

                if data['type'] in ['note_on', 'note_off']:
                    
                    # Release shift key
                    if data['note'] == 105 and data['velocity'] == 127:
                        return

                    # Enter
                    elif data['note'] == 41:
                        if data['velocity'] == 127:
                            d_translator.light_on(self.midiout_launchcontrol, 24, 'green')
                            translator.enter(self.midiout_external)
                        else:
                            d_translator.light_on(self.midiout_launchcontrol, 24, 'green_low')

                    # Tab
                    elif data['note'] == 43:
                        if data['velocity'] == 127:
                            d_translator.light_on(self.midiout_launchcontrol, 26, 'green')
                            translator.tab(self.midiout_external)
                        else:
                            d_translator.light_on(self.midiout_launchcontrol, 26, 'green_low')

                    # Mute
                    elif data['note'] == 106 and data['velocity'] == 127:
                        state.current_window = 'mixer'
                        self.light_right_panel_shift()

                    # Solo
                    elif data['note'] == 107 and data['velocity'] == 127:
                        state.current_window = 'pattern'
                        translator.activate_pattern_window(self.midiout_external)
                        self.light_right_panel_shift()

                    # Record Arm
                    elif data['note'] == 108 and data['velocity'] == 127:
                        state.current_window = 'browser'
                        translator.activate_browser_window(self.midiout_external)
                        self.light_right_panel_shift()

                    # Up
                    elif data['note'] == 42 and data['velocity'] == 127:
                        self.hold_cursor_up()

                    # Pan
                    elif data['note'] == 44 and data['velocity'] == 127:
                        self.reset_knob_panel()
                        d_translator.light_on(self.midiout_launchcontrol, 27, 'yellow')
                        translator.pan(self.midiout_external)

                    # Stereo
                    elif data['note'] == 57 and data['velocity'] == 127:
                        self.reset_knob_panel()
                        d_translator.light_on(self.midiout_launchcontrol, 28, 'yellow')
                        translator.stereo(self.midiout_external)

                    # Sends
                    elif data['note'] == 58 and data['velocity'] == 127:
                        self.reset_knob_panel()
                        d_translator.light_on(self.midiout_launchcontrol, 29, 'yellow')
                        translator.sends(self.midiout_external)

                    # Effect
                    elif data['note'] == 59 and data['velocity'] == 127:
                        self.reset_knob_panel()
                        d_translator.light_on(self.midiout_launchcontrol, 30, 'yellow')
                        translator.effect(self.midiout_external)

                    # EQ
                    elif data['note'] == 60 and data['velocity'] == 127:
                        self.reset_knob_panel()
                        d_translator.light_on(self.midiout_launchcontrol, 31, 'yellow')
                        translator.eq(self.midiout_external)

                    # Down
                    elif data['note'] == 74 and data['velocity'] == 127:
                        self.hold_cursor_down()

                    # Left
                    elif data['note'] == 73 and data['velocity'] == 127:
                        self.hold_cursor_left()

                    # Right
                    elif data['note'] == 75 and data['velocity'] == 127:
                        self.hold_cursor_right()

                    # <<
                    elif data['note'] == 76:
                        if data['velocity'] == 127:
                            d_translator.light_on(self.midiout_launchcontrol, 35, 'amber')
                            translator.rewind(self.midiout_external)
                        else:
                            d_translator.light_on(self.midiout_launchcontrol, 35, 'amber_low')
                            translator.rewind_off(self.midiout_external)

                    # >>
                    elif data['note'] == 89:
                        if data['velocity'] == 127:
                            d_translator.light_on(self.midiout_launchcontrol, 36, 'amber')
                            translator.forward(self.midiout_external)
                        else:
                            d_translator.light_on(self.midiout_launchcontrol, 36, 'amber_low')
                            translator.forward_off(self.midiout_external)
                    
                    # Stop
                    elif data['note'] == 90:
                        if data['velocity'] == 127:
                            translator.stop(self.midiout_external)
                            d_translator.light_on(self.midiout_launchcontrol, 37, 'red')
                            d_translator.light_on(self.midiout_launchcontrol, 38, 'green_low')
                    
                        else:
                            d_translator.light_on(self.midiout_launchcontrol, 37, 'red_low')

                    # Play
                    elif data['note'] == 91:
                        if data['velocity'] == 127:
                            translator.play(self.midiout_external)
                            d_translator.light_on(self.midiout_launchcontrol, 38, 'green')
                            d_translator.light_on(self.midiout_launchcontrol, 37, 'red_low')

                    # Record
                    elif data['note'] == 92:
                        if data['velocity'] == 127:
                            translator.record(self.midiout_external)

                            if state.rec_status:
                                d_translator.light_on(self.midiout_launchcontrol, 39, 'red_low')
                            else:
                                d_translator.light_on(self.midiout_launchcontrol, 39, 'red')

                            state.rec_status = not state.rec_status
                            print(state.rec_status)

                # Control change
                elif data['type'] == 'control_change':

                    # Preserve fader movement
                    if data['control'] in self.faders:
                        # Send the fader movement
                        translator.move_fader(self.midiout_external, data['value'], data['control'])

                    elif data['control'] in self.knobs:
                        translator.move_knob(self.midiout_external, data['value'], data['control'])

                    # Check arrow keys
                    self.arrow_keys(data)

            time.sleep(self.default_timeout)

    def refresh_bottom_row_mute(self):

        for value, index in zip(state.mute_status, range(8)):
            if value:
                d_translator.light_on_mute(self.midiout_launchcontrol, index+16)
            else:
                d_translator.light_off_mute(self.midiout_launchcontrol, index+16)

    def refresh_bottom_row_solo(self):

        for value, index in zip(state.solo_status, range(8)):
            if value:
                d_translator.light_on_mute(self.midiout_launchcontrol, index+16)
            else:
                d_translator.light_off_mute(self.midiout_launchcontrol, index+16)

    def refresh_bottom_row_arm(self):

        for value, index in zip(state.arm_status, range(8)):
            if value:
                d_translator.light_on_arm(self.midiout_launchcontrol, index)
            else:
                d_translator.light_off_arm(self.midiout_launchcontrol, index)

    def light_right_panel(self):

        if state.current_mode == 'mute':
            d_translator.light_on_mute_btn(self.midiout_launchcontrol)
        else:
            d_translator.light_off_mute_btn(self.midiout_launchcontrol)

        if state.current_mode == 'solo':
            d_translator.light_on_solo_btn(self.midiout_launchcontrol)
        else: 
            d_translator.light_off_solo_btn(self.midiout_launchcontrol)

        if state.current_mode == 'arm':
            d_translator.light_on_arm_btn(self.midiout_launchcontrol)  
        else: 
            d_translator.light_off_arm_btn(self.midiout_launchcontrol)

    def light_right_panel_shift(self):

        if state.current_window == 'mixer':
            d_translator.light_on_mute_btn(self.midiout_launchcontrol)
        else:
            d_translator.light_off_mute_btn(self.midiout_launchcontrol)

        if state.current_window == 'pattern':
            d_translator.light_on_solo_btn(self.midiout_launchcontrol)
        else: 
            d_translator.light_off_solo_btn(self.midiout_launchcontrol)

        if state.current_window == 'browser':
            d_translator.light_on_arm_btn(self.midiout_launchcontrol)  
        else: 
            d_translator.light_off_arm_btn(self.midiout_launchcontrol)   
            
    def restore_screen_state(self):
        # Light right panel
        self.light_right_panel()
        self.lower_panel()
        self.upper_panel()

    def light_on_device(self):
        d_translator.light_on_device(self.midiout_launchcontrol)

    def light_off_device(self):
        d_translator.light_off_device(self.midiout_launchcontrol)

    def arrow_keys(self, data):

        # ^
        if data['control'] == 104 and data['value'] == 127:
            if state.current_window == 'mixer':
                translator.bank_left(self.midiout_external)

            elif state.current_window == 'pattern':
                translator.channel_up(self.midiout_external)

            elif state.current_window == 'browser':
                translator.browser_up(self.midiout_external)

        # v
        elif data['control'] == 105 and data['value'] == 127:
            if state.current_window == 'mixer':
                translator.bank_right(self.midiout_external)

            elif state.current_window == 'pattern':
                translator.channel_down(self.midiout_external)

            elif state.current_window == 'browser':
                translator.browser_down(self.midiout_external)

        # <
        elif data['control'] == 106 and data['value'] == 127:
            if state.current_window == 'mixer':
                translator.mixer_channel_left(self.midiout_external)

            elif state.current_window == 'pattern':                          
                translator.move_channel_up(self.midiout_external)

            elif state.current_window == 'browser':
                translator.browser_left(self.midiout_external)

        # >
        elif data['control'] == 107 and data['value'] == 127:
            if state.current_window == 'mixer':
                translator.mixer_channel_right(self.midiout_external)

            elif state.current_window == 'pattern':
                translator.move_channel_down(self.midiout_external)

            elif state.current_window == 'browser':
                translator.browser_right(self.midiout_external)

    def lower_panel_shift(self):
        
        # Initialize the rows
        top_row = [None] * 8
        lower_row = [None] * 8

        # Enter
        top_row [0] = 'green_low'
        top_row [2] = 'green_low'

        # Highlight arrows
        top_row [1] = 'yellow_low'
        lower_row[0] = 'yellow_low'
        lower_row[1] = 'yellow_low'
        lower_row[2] = 'yellow_low'

        # Transport
        lower_row[3] = 'yellow_low'
        lower_row[4] = 'yellow_low'
        lower_row[5] = 'red_low'
        lower_row[6] = 'green_low'
        lower_row[7] = 'red_low'

        if state.play_status:
            lower_row[5] = 'red'

        if state.play_status:
            lower_row[6] = 'green'

        if state.play_status:
            lower_row[7] = 'red'

        # Knob mode
        top_row [3] = 'yellow_low'
        top_row [4] = 'yellow_low'
        top_row [5] = 'yellow_low'
        top_row [6] = 'yellow_low'
        top_row [7] = 'yellow_low'

        if state.knob_mode == 'pan':
            top_row [3] = 'yellow'

        elif state.knob_mode == 'stereo':
            top_row [3] = 'yellow'

        if state.knob_mode == 'sends':
            top_row [3] = 'yellow'

        if state.knob_mode == 'effect':
            top_row [3] = 'yellow'

        if state.knob_mode == 'eq':
            top_row [3] = 'yellow'

        # Send the panel
        for value, index in zip(top_row, range(24, 32)):
            d_translator.light_on(self.midiout_launchcontrol, index, value)

        for value, index in zip(lower_row, range(32, 40)):
            d_translator.light_on(self.midiout_launchcontrol, index, value)

    def lower_panel(self):

        if state.current_mode == 'mute':
            self.refresh_bottom_row_mute()

        elif state.current_mode == 'solo':
            self.refresh_bottom_row_solo()

        elif state.current_mode == 'arm':
            self.refresh_bottom_row_arm()

    def upper_panel(self):

        for value, index in zip(state.channel_focus, range(24, 32)):
            d_translator.light_on(self.midiout_launchcontrol, index, value)

    def activate_channel(self, note):
        
        values = {
            41: 0,
            42: 1,
            43: 2,
            44: 3,
            57: 4,
            58: 5,
            59: 6,
            60: 7
        }

        translator.activate_channel(self.midiout_external, values[note])
        
    def hold_cursor_up(self):

        d_translator.light_on(self.midiout_launchcontrol, 25, 'amber')

        while self.keep_running:

            # Get the message
            message = self.midiin_launchcontrol.poll()

            if message:

                # Organize the values
                data = message.dict()

                if data['note'] == 42 and data['velocity'] == 0:
                    d_translator.light_on(self.midiout_launchcontrol, 25, 'amber_low')
                    return
                
            
            translator.cursor_up(self.midiout_external)

            time.sleep(0.1)

    def hold_cursor_down(self):

        d_translator.light_on(self.midiout_launchcontrol, 33, 'amber')

        while self.keep_running:

            # Get the message
            message = self.midiin_launchcontrol.poll()

            if message:

                # Organize the values
                data = message.dict()

                if data['note'] == 74 and data['velocity'] == 0:
                    d_translator.light_on(self.midiout_launchcontrol, 33, 'amber_low')
                    return
                
            
            translator.cursor_down(self.midiout_external)

            time.sleep(0.1)

    def hold_cursor_left(self):

        d_translator.light_on(self.midiout_launchcontrol, 32, 'amber')

        while self.keep_running:

            # Get the message
            message = self.midiin_launchcontrol.poll()

            if message:

                # Organize the values
                data = message.dict()

                if data['note'] == 73 and data['velocity'] == 0:
                    d_translator.light_on(self.midiout_launchcontrol, 32, 'amber_low')
                    return
                
            
            translator.cursor_left(self.midiout_external)

            time.sleep(0.1)
    
    def hold_cursor_right(self):

        d_translator.light_on(self.midiout_launchcontrol, 34, 'amber')

        while self.keep_running:

            # Get the message
            message = self.midiin_launchcontrol.poll()

            if message:

                # Organize the values
                data = message.dict()

                if data['note'] == 75 and data['velocity'] == 0:
                    d_translator.light_on(self.midiout_launchcontrol, 34, 'amber_low')
                    return
                
            
            translator.cursor_right(self.midiout_external)

            time.sleep(0.1)

    def reset_knob_panel(self):
        d_translator.light_on(self.midiout_launchcontrol, 27, 'yellow_low')
        d_translator.light_on(self.midiout_launchcontrol, 28, 'yellow_low')
        d_translator.light_on(self.midiout_launchcontrol, 29, 'yellow_low')
        d_translator.light_on(self.midiout_launchcontrol, 30, 'yellow_low')
        d_translator.light_on(self.midiout_launchcontrol, 31, 'yellow_low')
