import tkinter as tk
from tkinter import ttk

import midi_manager as mm

class MainWindow(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.create_variables()
        self.create_widgets()
        self.position_widgets()
        self.setup_widgets()
        self.add_callbacks()

        self.pack(fill=tk.BOTH)

    def create_variables(self):
        self.var_lc_input = tk.StringVar(self)
        self.var_lc_input.set("Select One")

        self.var_lc_output = tk.StringVar(self)
        self.var_lc_output.set("Select One")

        self.var_ext_output = tk.StringVar(self)
        self.var_ext_output.set("Select One")

        self.var_ext_input = tk.StringVar(self)
        self.var_ext_input.set("Select One")

        # Store the variables for frames in an array
        self.vars_faders = [tk.IntVar(self) for i in range(8)]
        self.vars_knobs = [tk.IntVar(self) for i in range(8)]
        self.var_fader_master = tk.IntVar(self)

        #self.var_volume_scale_translated = tk.StringVar(self)

    def create_widgets(self):

        # Frames
        self.frame_top = ttk.Frame(self)
        self.frame_middle = ttk.Frame(self)

        # Midi panel
        self.frame_midi = ttk.LabelFrame(self.frame_top, text="Midi Settings")
        self.frame_channels = ttk.Frame(self.frame_middle)
        self.frame_channel = [ttk.LabelFrame(self.frame_channels, text="Channel " + str(i)) for i in range(8)]

        self.label_lp_input = ttk.Label(self.frame_midi, text="Launchcontrol XL Input Device:")
        self.label_lp_output = ttk.Label(self.frame_midi, text="Launchcontrol XL Output Device:")
        self.label_ext_input = ttk.Label(self.frame_midi, text="Virtual MIDI Input Device:")
        self.label_ext_output = ttk.Label(self.frame_midi, text="Virtual MIDI Output Device:")
   
        self.dpw_lp_input = ttk.OptionMenu(self.frame_midi, self.var_lc_input, *(["Select One"] + mm.get_input_port_names()))
        self.dpw_lp_output = ttk.OptionMenu(self.frame_midi, self.var_lc_output, *(["Select One"] + mm.get_output_port_names()))
        self.dpw_ext_input = ttk.OptionMenu(self.frame_midi, self.var_ext_input, *(["Select One"] + mm.get_input_port_names()))
        self.dpw_ext_output = ttk.OptionMenu(self.frame_midi, self.var_ext_output, *(["Select One"] + mm.get_output_port_names()))

        # Channel slides
        self.pan_knobs = [None]*8
        self.solo_buttons = [None]*8
        self.mute_buttons = [None]*8
        self.select_buttons = [None]*8
        self.scales_faders = [None]*8

        for i in range(8):
            self.pan_knobs[i] = ttk.Scale(self.frame_channel[i], variable=self.vars_knobs[i], from_=0, to=127, orient=tk.HORIZONTAL)
            self.solo_buttons[i] = tk.Button(self.frame_channel[i], text="SOLO")
            self.mute_buttons[i] = tk.Button(self.frame_channel[i], text="MUTE")
            self.select_buttons[i] = tk.Button(self.frame_channel[i], text="SELECT")
            self.scales_faders[i] = ttk.Scale(self.frame_channel[i], variable=self.vars_faders[i], from_=-8192, to=8176, orient=tk.VERTICAL)

        # vpot assign buttons
        self.frame_master = ttk.Frame(self.frame_middle)

        self.frame_vpot_0 = ttk.LabelFrame(self.frame_master, text="VPOT ASSIGN")
        self.frame_vpot_1 = ttk.Frame(self.frame_vpot_0)
        self.frame_vpot_2 = ttk.Frame(self.frame_vpot_0)
        self.frame_vpot_3 = ttk.Frame(self.frame_vpot_0)

        self.frame_banks_0 = ttk.LabelFrame(self.frame_master, text="FADER_BANKS")
        self.frame_banks_1 = ttk.Frame(self.frame_banks_0)
        self.frame_banks_2 = ttk.Frame(self.frame_banks_0)
        self.frame_banks_3 = ttk.Frame(self.frame_banks_0)

        self.btn_track = tk.Button(self.frame_vpot_1, text="TRACK")
        self.btn_send = tk.Button(self.frame_vpot_1, text="SEND")
        self.btn_pan_surround = tk.Button(self.frame_vpot_2, text="PAN/SURROUND")
        self.btn_plug_in = tk.Button(self.frame_vpot_2, text="PLUG-IN")
        self.btn_eq = tk.Button(self.frame_vpot_3, text="EQ")
        self.btn_instrument = tk.Button(self.frame_vpot_3, text="INSTRUMENT")

        self.btn_bank_left = tk.Button(self.frame_banks_1, text="< BANK")
        self.btn_bank_right = tk.Button(self.frame_banks_1, text="BANK >")
        self.btn_channel_left = tk.Button(self.frame_banks_2, text="< CHANNEL")
        self.btn_channel_right = tk.Button(self.frame_banks_2, text="CHANNEL >")
        self.btn_flip = tk.Button(self.frame_banks_3, text="FLIP")
        self.btn_global_view = tk.Button(self.frame_banks_3, text="GLOBAL VIEW")

        self.scale_fader_master = ttk.Scale(self.frame_master, variable=self.var_fader_master, from_=-8192, to=8176, orient=tk.VERTICAL)

        # List Boxes
        #self.scroll_modes = tk.Scrollbar(self.frame_modes, orient="vertical")

        #self.lstb_listbox_modes = tk.Listbox(self.frame_modes, yscrollcommand=self.scroll_modes.set)
        #for mode in mom.modes:
        #    self.lstb_listbox_modes.insert(tk.END, mode.properties['name'])
        #
       #self.scroll_modes.config(command=self.lstb_listbox_modes.yview)

        # Scales

    def position_widgets(self):

        # Main frames
        self.frame_top.pack(fill=tk.X)
        self.frame_middle.pack(fill=tk.X)
        self.frame_master.pack(fill=tk.X)

        # Midi Frame
        self.frame_midi.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)
        self.label_lp_input.pack(fill=tk.X, padx=5, pady=2)
        self.dpw_lp_input.pack(fill=tk.X, padx=5, pady=2)
        self.label_lp_output.pack(fill=tk.X, padx=5, pady=2)
        self.dpw_lp_output.pack(fill=tk.X, padx=5, pady=2)
        self.label_ext_input.pack(fill=tk.X, padx=5, pady=2)
        self.dpw_ext_input.pack(fill=tk.X, padx=5, pady=2)
        self.label_ext_output.pack(fill=tk.X, padx=5, pady=2)
        
        # Volume faders
        for i in range(8):
            self.frame_channel[i].pack(fill=tk.Y, padx=5, pady=5, side=tk.LEFT)
            self.pan_knobs[i].pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)
            self.solo_buttons[i].pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)
            self.mute_buttons[i].pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)
            self.select_buttons[i].pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)
            self.scales_faders[i].pack(fill=tk.Y, padx=5, pady=5, ipadx=5, ipady=5)

        self.frame_channels.pack(fill=tk.Y, side=tk.LEFT)

        # Vpot panel
        self.btn_track.pack(fill=tk.X, padx=5, pady=5, side=tk.LEFT)
        self.btn_send.pack(fill=tk.X, padx=5, pady=5, side=tk.RIGHT)
        self.btn_pan_surround.pack(fill=tk.X, padx=5, pady=5, side=tk.LEFT)
        self.btn_plug_in.pack(fill=tk.X, padx=5, pady=5, side=tk.RIGHT)
        self.btn_eq.pack(fill=tk.X, padx=5, pady=5, side=tk.LEFT)
        self.btn_instrument.pack(fill=tk.X, padx=5, pady=5, side=tk.RIGHT)

        self.frame_vpot_1.pack(fill=tk.X)
        self.frame_vpot_2.pack(fill=tk.X)
        self.frame_vpot_3.pack(fill=tk.X)
        self.frame_vpot_0.pack(fill=tk.X, pady=5, ipady=5)
        
        # Fader Bank panel
        self.btn_bank_left.pack(fill=tk.X, padx=5, pady=5, side=tk.LEFT)
        self.btn_bank_right.pack(fill=tk.X, padx=5, pady=5, side=tk.RIGHT)
        self.btn_channel_left.pack(fill=tk.X, padx=5, pady=5, side=tk.LEFT)
        self.btn_channel_right.pack(fill=tk.X, padx=5, pady=5, side=tk.RIGHT)
        self.btn_flip.pack(fill=tk.X, padx=5, pady=5, side=tk.LEFT)
        self.btn_global_view.pack(fill=tk.X, padx=5, pady=5, side=tk.RIGHT)

        self.frame_banks_1.pack(fill=tk.X)
        self.frame_banks_2.pack(fill=tk.X)
        self.frame_banks_3.pack(fill=tk.X)
        self.frame_banks_0.pack(fill=tk.X, pady=5, ipady=5)

        self.scale_fader_master.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)

        # Master fader
        self.frame_master.pack(side=tk.RIGHT)
        
        
        self.frame_middle.pack(side=tk.LEFT)
        


    def setup_widgets(self):
        pass

    def add_callbacks(self):
        pass
        #self.var_lc_input.trace_add("write", self.callback_lp_input)
        #self.var_lc_output.trace_add("write", self.callback_lp_output)
        #self.var_ext_output.trace_add("write", self.callback_ext_output)

        #self.lstb_listbox_modes.bind('<<ListboxSelect>>', self.callback_listbox_modes)

    #def callback_update_volume(self, *args):
    #    ctrl.set_volume_position(self.var_volume_scale.get())
    #    self.var_volume_scale_translated.set(maps.volume_positions[int(self.var_volume_scale.get())])