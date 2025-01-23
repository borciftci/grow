# need package python-rtmidi
import time
import rtmidi as midi

out = midi.MidiOut()

ports = out.get_ports()  # output: ['Microsoft GS Wavetable Synth 0']

out.open_port(0)

with out:
    note_on = [0x94, 48, 112]
    note_off = [0x84, 48, 0]

    # Set the filter to 0
    cc_msg = [0xB4, 3, 0]  # parameter 3 is the filter cutoff in op-z 1
    out.send_message(cc_msg)
    time.sleep(0.1)

    # Set note on
    out.send_message(note_on)
    time.sleep(1)

    # Start ramping filter
    for cc in range(127):
        cc_msg = [0xB4, 3, cc]
        out.send_message(cc_msg)
        time.sleep(0.1)

    # Set note off
    out.send_message(note_off)
    time.sleep(0.1)

