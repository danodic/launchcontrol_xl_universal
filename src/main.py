import time

import midi_manager as mm
from controller_input_thread import ControllerInputThread
from daw_input_thread import DawInputThread

print(mm.get_input_port_names())
print(mm.get_output_port_names())

midiin_external = mm.get_input_port("mcu output 7")
midiin_launchcontrol = mm.get_input_port("Launch Control XL 16")
midiout_external = mm.get_output_port("mcu input 8")
midiout_launchcontrol = mm.get_output_port("Launch Control XL 18")

input_thread_c = ControllerInputThread(midiin_launchcontrol, midiin_external, midiout_launchcontrol, midiout_external)
input_thread_d = DawInputThread(midiin_launchcontrol, midiin_external, midiout_launchcontrol, midiout_external)

input_thread_c.daemon = True
input_thread_d.daemon = True
input_thread_c.start()
input_thread_d.start()

while True:
    time.sleep(1)