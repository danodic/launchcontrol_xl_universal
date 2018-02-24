import threading
import time
import mido
import pdb

import daw_translator as translator
import controller_status as state

class DawInputThread (threading.Thread):
    """

    """

    def __init__(self, midiin_launchcontrol=None, midiin_external=None, midiout_launchcontrol=None, midiout_external=None):
        """
        TODO
        """

        self.default_timeout = 0.0001
        self.tick_sum = 0

        # Initialize the threading lib
        threading.Thread.__init__(self)

        # Store some variables
        self.midiin_external = midiin_external
        self.midiin_launchcontrol = midiin_launchcontrol
        self.midiout_external = midiout_external
        self.midiout_launchcontrol = midiout_launchcontrol
        self.keep_running = True
        self.running = False

        # Values
        self.channel_select = [24, 25, 26, 27, 28, 29, 30, 31]
        self.record_arm = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.mute = [16, 17, 18, 19, 20 ,21 ,22, 23]

    def run(self):
        self.wait_for_midi_devices()

        if not self.keep_running:
            return

        self.running = True
        self.screen_main()

    def wait_for_midi_devices(self):
        while (self.midiin_launchcontrol is None or self.midiin_external is None or self.midiout_external is None or self.midiout_launchcontrol is None) and self.keep_running:
            time.sleep(self.default_timeout)

    def screen_main(self):
        """

        """

        #self.knob_leds_off()

        while self.keep_running:

            # Get the message
            message = self.midiin_external.poll()

            if message:

                # Organize the values
                data = message.dict()

                #print("input", data)

                # Clock
                #if data['type'] == 'clock' and data['time'] == 0:

                #    if self.tick_sum == 0:
                #        self.light_next_knob()

                #    self.tick_sum += 1

                #    if self.tick_sum == 12:
                #        self.tick_sum = 0

                # Note
                if data['type'] == 'note_on':
                    
                    # Track focus key
                    if data['note'] in self.channel_select and data['velocity'] == 127:
                        translator.light_on_track_focus(self.midiout_launchcontrol, data['note'])

                    elif data['note'] in self.channel_select and data['velocity'] == 0:
                        translator.light_off_track_focus(self.midiout_launchcontrol, data['note'])

                    # Mute/Solo
                    elif data['note'] in self.mute:

                        translator.store_mute_solo_status(data['note'], data['velocity'])
                        
                        if data['velocity'] == 127:
                            if state.current_mode == 'mute':
                                translator.light_on_mute(self.midiout_launchcontrol, data['note'])
                            
                            elif state.current_mode == 'solo':
                                translator.light_off_mute(self.midiout_launchcontrol, data['note'])

                        elif data['velocity'] == 0:
                            if state.current_mode == 'mute':
                                translator.light_off_mute(self.midiout_launchcontrol, data['note'])

                            elif state.current_mode == 'solo':
                                translator.light_on_mute(self.midiout_launchcontrol, data['note'])
                        
                    # Record/Arm
                    elif data['note'] in self.record_arm:

                        translator.store_arm_status(data['note'], data['velocity'])
                    
                        if data['velocity'] == 127 and state.current_mode == 'arm':
                            translator.light_on_arm(self.midiout_launchcontrol, data['note'])

                        elif data['velocity'] == 0 and state.current_mode == 'arm':
                            translator.light_off_arm(self.midiout_launchcontrol, data['note'])

            time.sleep(self.default_timeout)

    def knob_leds_off(self):

        for i in range(16, 24):
            translator.light_on(self.midiout_launchcontrol, i, 'off')
        
        state.knob_leds = 0

    def light_next_knob(self):
        translator.light_on(self.midiout_launchcontrol, 16+state.knob_leds, 'amber')
        
        if state.knob_leds == 0:
            translator.light_on(self.midiout_launchcontrol, 16+7, 'off')
        else:
            translator.light_on(self.midiout_launchcontrol, 16+state.knob_leds-1, 'off')

        state.knob_leds += 1

        if state.knob_leds == 8:
            state.knob_leds = 0