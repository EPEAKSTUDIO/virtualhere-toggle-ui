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

        # Create a frame to hold the toggle and notifications at the center of the screen
        center_frame = ttk.Frame(self.root)
        center_frame.pack(expand=True)

        # Configure the vertical space to take about 70% of the screen's height
        center_frame.grid_rowconfigure(0, weight=7)
        center_frame.grid_rowconfigure(1, weight=3)

        # Create the on/off toggle button
        self.toggle_var = tk.BooleanVar()
        self.toggle_button = ttk.Checkbutton(
            center_frame,
            text="VirtualHere Service",
            variable=self.toggle_var,
            command=self.on_toggle_change,
            style="Toggle.TCheckbutton"
        )
        self.toggle_button.pack(expand=True)

        # Create the text notification label (initially empty)
        self.notification_label = ttk.Label(
            center_frame,
            text="",
            font=("Helvetica", 12)
        )
        self.notification_label.pack(expand=True)

        # Set the initial position of the toggle based on the service status
        self.set_initial_toggle_position()

    def on_toggle_change(self):
        # Handle the action when the toggle is switched on/off
        if self.toggle_var.get():
            self.notification_label.config(text="Starting service...")
            try:
                subprocess.run(['sudo', 'systemctl', 'start', 'virtualhere.service'], check=True)
                self.notification_label.config(text="Service started successfully.")
            except subprocess.CalledProcessError:
                self.notification_label.config(text="Failed to start service.")
                self.toggle_var.set(False)  # Set the toggle back to "OFF"
        else:
            self.notification_label.config(text="Stopping service...")
            try:
                subprocess.run(['sudo', 'systemctl', 'stop', 'virtualhere.service'], check=True)
                self.notification_label.config(text="Service stopped successfully.")
            except subprocess.CalledProcessError:
                self.notification_label.config(text="Failed to stop service.")

        # Update the toggle button to reflect the new status
        self.toggle_button.config(text="VirtualHere Service" + (" ON" if self.toggle_var.get() else " OFF"))
        self.notification_label.after(2000, lambda: self.notification_label.config(text=""))

    def set_initial_toggle_position(self):
        # Get the initial status of the service from systemctl
        try:
            result = subprocess.run(['systemctl', 'is-active', 'virtualhere.service'], capture_output=True, text=True, check=True)
            initial_status = (result.stdout.strip() == "active")
        except subprocess.CalledProcessError:
            # In case of an error (e.g., service not found), assume the service is inactive
            initial_status = False

        # Set the initial position of the toggle and update the UI accordingly
        self.toggle_var.set(initial_status)
        self.toggle_button.config(text="VirtualHere Service" + (" ON" if initial_status else " OFF"))

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
