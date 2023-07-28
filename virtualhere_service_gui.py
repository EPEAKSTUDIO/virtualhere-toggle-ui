import tkinter as tk
from tkinter import ttk
import subprocess

class VirtualHereToggleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VirtualHere Toggle UI")
        self.root.geometry("400x600")  # Set the initial window size

        # Center the window on the screen
        self.root.eval('tk::PlaceWindow . center')

        # Configure the vertical space to take about 70% of the screen's height
        self.root.grid_rowconfigure(0, weight=7)
        self.root.grid_rowconfigure(1, weight=3)

        # Create the on/off toggle button
        self.toggle_var = tk.BooleanVar()
        self.toggle_button = ttk.Checkbutton(
            self.root,
            text="VirtualHere Service",
            variable=self.toggle_var,
            command=self.on_toggle_change,
            style="Toggle.TCheckbutton"
        )
        self.toggle_button.grid(row=0, column=0, sticky="nsew")

        # Create the text notification label (initially empty)
        self.notification_label = ttk.Label(
            self.root,
            text="",
            font=("Helvetica", 12)
        )
        self.notification_label.grid(row=1, column=0, sticky="nsew")

        # Create the close button (X symbol)
        close_btn = tk.Label(
            self.root,
            text="X",
            font=("Helvetica", 12, "bold"),
            fg="red",
            cursor="hand2"
        )
        close_btn.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        close_btn.bind("<Button-1>", self.close_app)

        # Set the initial position of the toggle based on the service status (change this according to your logic)
        self.set_initial_toggle_position()  # Add your logic to determine the initial status

    def on_toggle_change(self):
        # Handle the action when the toggle is switched on/off
        if self.toggle_var.get():
            self.notification_label.config(text="Starting service...")
            # Add the action to start the virtualhere.service here (async if needed)
            self.notification_label.after(2000, lambda: self.notification_label.config(text=""))
        else:
            self.notification_label.config(text="Stopping service...")
            # Add the action to stop the virtualhere.service here (async if needed)
            self.notification_label.after(2000, lambda: self.notification_label.config(text=""))

    def set_initial_toggle_position(self):
        # Add your logic here to determine the initial status of the service (e.g., is it running or stopped)
        # Based on the status, set the initial position of the toggle_var and update the UI accordingly.
        # Example:
        initial_status = True  # Set this to True or False based on the actual status
        self.toggle_var.set(initial_status)

        if initial_status:
            self.notification_label.config(text="Starting service...")
            # Add the action to start the virtualhere.service here (async if needed)
            self.notification_label.after(2000, lambda: self.notification_label.config(text=""))
        else:
            self.notification_label.config(text="Stopping service...")
            # Add the action to stop the virtualhere.service here (async if needed)
            self.notification_label.after(2000, lambda: self.notification_label.config(text=""))

    def close_app(self, event):
        # Action to close the application gracefully
        self.root.destroy()

def main():
    root = tk.Tk()
    root.style = ttk.Style()
    root.style.configure("Toggle.TCheckbutton", background="#4CAF50", foreground="white", font=("Helvetica", 20, "bold"))

    app = VirtualHereToggleUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
