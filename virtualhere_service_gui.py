import tkinter as tk
from tkinter import ttk
import subprocess

class VirtualHereToggleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VirtualHere Toggle UI")
        self.root.geometry("480x320")  # Set the initial window size

        # Center the window on the screen
        self.root.eval('tk::PlaceWindow . center')

        # Create a canvas with a green background (80% of the screen resolution)
        canvas_width = int(self.root.winfo_screenwidth() * 0.8)
        canvas_height = int(self.root.winfo_screenheight() * 0.8)
        self.canvas = tk.Canvas(self.root, bg="#4CAF50", width=canvas_width, height=canvas_height, highlightthickness=0)
        self.canvas.pack(expand=True)

        # Create the on/off toggle button
        self.toggle_var = tk.BooleanVar()
        self.toggle_button = ttk.Checkbutton(
            self.canvas,
            text="USB over IP",
            variable=self.toggle_var,
            command=self.on_toggle_change,
            style="Toggle.TCheckbutton"
        )
        self.toggle_button_window = self.canvas.create_window(canvas_width/2, canvas_height/2, anchor="center", window=self.toggle_button)

        # Create the text notification label (initially empty)
        self.notification_label = ttk.Label(
            self.canvas,
            text="",
            font=("Helvetica", 12)
        )
        self.notification_label_window = self.canvas.create_window(canvas_width/2, canvas_height * 0.9, anchor="center", window=self.notification_label)

        # Create the close button (red cross)
        close_btn = tk.Label(
            self.canvas,
            text="X",
            font=("Helvetica", 12, "bold"),
            fg="red",
            cursor="hand2"
        )
        close_btn_window = self.canvas.create_window(canvas_width - 20, 20, anchor="ne", window=close_btn)
        close_btn.bind("<Button-1>", self.close_app)

        # Bind the click event to the canvas
        self.canvas.bind("<Button-1>", self.on_toggle_change)

        # Set the initial position of the toggle based on the service status (change this according to your logic)
        self.set_initial_toggle_position()  # Add your logic to determine the initial status

    # ... Rest of the code remains the same

def main():
    root = tk.Tk()
    root.style = ttk.Style()
    root.style.configure("Toggle.TCheckbutton", background="#4CAF50", foreground="white", font=("Helvetica", 20, "bold"))
    root.style.map("Toggle.TCheckbutton",
                   foreground=[("active", "white"), ("!active", "white")],
                   background=[("active", "orange"), ("!active", "#4CAF50")])
    root.style.configure("Toggle.TCheckbuttonOn", background="red")
    root.style.configure("Toggle.TCheckbuttonOff", background="green")

    app = VirtualHereToggleUI(root)

    # Set the application to start in fullscreen mode
    root.attributes("-fullscreen", True)

    root.mainloop()

if __name__ == "__main__":
    main()
