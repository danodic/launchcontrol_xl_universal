import time

import midi_manager as mm

print(mm.get_input_port_names())
print(mm.get_output_port_names())

midiin_external_name = "mcu output 7"
midiin_control_name = "DESKTOP-VTEI351 4"
midiout_external_name = "mcu input 8"
midiout_control_name = "DESKTOP-VTEI351 6"

midiin_external = mm.get_input_port(midiin_external_name)
midiin_control = mm.get_input_port(midiin_control_name)
midiout_external = mm.get_output_port(midiout_external_name)
midiout_control = mm.get_output_port(midiout_control_name)

while True:

    # Get the message
    message_external_in = midiin_external.poll()
    message_control_in = midiin_control.poll()

    if message_external_in:
        message = message_external_in  
        print("input " + midiin_external_name, message.dict())
        
        midiout_control.send(message)

    if message_control_in:
        message = message_control_in
        print("input " + midiin_control_name, message.dict())

        midiout_external.send(message)

    time.sleep(0.000001)