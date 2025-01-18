import tkinter as tk
from tkinter import ttk
from sound.generator import SoundGenerator
from visuals.tree import Tree


class SoundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ambient Sound Generator")
        self.root.geometry("800x600")  # Fixed window size
        self.root.resizable(False, False)  # Prevent resizing

        self.sound_generator = SoundGenerator()

        # Note and frequency data
        self.notes = self.sound_generator.notes
        self.frequencies = self.sound_generator.frequencies
        self.is_updating = False  # Guard variable to prevent recursion

        # Create a main frame for layout
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Create canvas for tree visualization
        self.canvas = tk.Canvas(main_frame, bg="white", width=800, height=400)
        self.canvas.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        # Tree class instance
        self.tree = Tree(self.canvas)

        # Create a frame for sliders and buttons
        controls_frame = tk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Configure grid weights for controls_frame
        controls_frame.grid_columnconfigure(0, weight=1)  # For sliders
        # controls_frame.grid_columnconfigure(1, weight=1)  # For sliders
        controls_frame.grid_columnconfigure(2, weight=4)  # For sliders to expand

        # Create a subframe for buttons
        buttons_frame = tk.Frame(controls_frame)
        buttons_frame.grid(row=0, column=0, padx=10, sticky="w")

        # Start Button
        self.start_button = ttk.Button(buttons_frame, text="Start", style="TButton", command=self.start_sound)
        self.start_button.pack(pady=5)

        # Stop Button
        self.stop_button = ttk.Button(buttons_frame, text="Stop", style="TButton", command=self.stop_sound)
        self.stop_button.pack(pady=5)

        # Create a subframe for sliders
        sliders_frame = tk.Frame(controls_frame)
        sliders_frame.grid(row=0, column=1, columnspan=2, padx=10, sticky="ew")

        # Tree iteration label
        self.iteration_label = tk.Label(sliders_frame, text="Iterations: 0", font=("Helvetica", 12))
        self.iteration_label.pack(anchor="w", pady=5)

        # Tree iteration slider
        self.iteration_slider = ttk.Scale(
            sliders_frame,
            from_=0,
            to=10,
            orient="horizontal",
            command=self.update_tree_iterations
        )
        self.iteration_slider.set(0)  # Default iterations
        self.iteration_slider.pack(fill="x", pady=5)

        # Frequency slider label
        self.slider_label = ttk.Label(sliders_frame, text="Note: A4 (440 Hz)", font=("Helvetica", 12))
        self.slider_label.pack(anchor="w")

        # Frequency slider
        self.frequency_slider = ttk.Scale(
            sliders_frame,
            from_=0,
            to=len(self.frequencies) - 1,
            orient="horizontal",
            command=self.update_frequency
        )
        self.frequency_slider.set(self.frequencies.index(440.0))  # Default to A4
        self.frequency_slider.pack(fill="x", pady=5)

        # Button styling
        self.style = ttk.Style()
        self.style.configure(
            "TButton",
            font=("Arial", 11),
            padding=8,
            foreground="#FFFFFF",
            background="#4CAF50",
        )
        self.style.map(
            "TButton",
            background=[("active", "#45A049")],  # Hover color
        )

    def update_tree_iterations(self, value):
        iterations = int(float(value))
        self.iteration_label.config(text=f"Iterations: {iterations}")
        self.tree.set_iterations(iterations)
        self.tree.generate_and_draw()

    def start_sound(self):
        index = round(self.frequency_slider.get())
        note = self.notes[index]  # Get the corresponding note
        self.sound_generator.start_sound(note)

    def stop_sound(self):
        self.sound_generator.stop_sound()

    def update_frequency(self, value):
        if self.is_updating:
            return  # Prevent recursion during slider update

        try:
            self.is_updating = True  # Start the update lock
            index = round(float(value))
            frequency = self.frequencies[index]
            note = self.notes[index]
            self.slider_label.config(text=f"Note: {note} ({frequency:.2f} Hz)")
            self.frequency_slider.set(index)  # Snap the slider to the nearest note
            # Update the frequency if the sound is playing
            if hasattr(self.sound_generator, "stream") and self.sound_generator.stream:
                self.sound_generator.frequency = frequency
        finally:
            self.is_updating = False  # Release the update lock


if __name__ == "__main__":
    root = tk.Tk()
    app = SoundApp(root)
    root.mainloop()
