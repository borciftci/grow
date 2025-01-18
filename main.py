import tkinter as tk
from gui.sound_gui import SoundApp

if __name__ == "__main__":
    # Create the main Tkinter application window
    root = tk.Tk()

    # Initialize the SoundApp, which contains the GUI and sound logic
    app = SoundApp(root)

    # Start the Tkinter event loop
    root.mainloop()