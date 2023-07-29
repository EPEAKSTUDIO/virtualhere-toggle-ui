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

        # Create a canvas with a green background (16:9 aspect ratio)
        self.canvas = tk.Canvas(self.root, bg="#4CAF50", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create the on/off toggle button
        self.toggle_var = tk.BooleanVar()
        self.toggle_button = ttk.Checkbutton(
            self.canvas,
            text="VirtualHere Service",
            variable=self.toggle_var,
            command=self.on_toggle_change,
            style="Toggle.TCheckbutton"
        )
        self.toggle_button_window = self.canvas.create_window(0, 0, anchor="nw", window=self.toggle_button)

        # Create the text notification label (initially empty)
        self.notification_label = ttk.Label(
            self.canvas,
            text="",
            font=("Helvetica", 12)
        )
        self.notification_label_window = self.canvas.create_window(0, 0, anchor="center", window=self.notification_label)

        # Bind the close event to the root
        self.root.bind("<Escape>", self.close_app)

        # Set the initial position of the toggle based on the service status (change this according to your logic)
        self.set_initial_toggle_position()  # Add your logic to determine the initial status

    def on_toggle_change(self):
        # Handle the action when the toggle is clicked
        self.toggle_var.set(not self.toggle_var.get())

        if self.toggle_var.get():
            self.notification_label.config(text="Starting service...", fg="orange")
            try:
                subprocess.run(['sudo', 'systemctl', 'start', 'virtualhere.service'], check=True)
                self.notification_label.config(text="Service started successfully.", fg="green")
            except subprocess.CalledProcessError:
                self.notification_label.config(text="Failed to start service.", fg="red")
                self.toggle_var.set(False)  # Set the toggle back to "OFF"
        else:
            self.notification_label.config(text="Stopping service...", fg="orange")
            try:
                subprocess.run(['sudo', 'systemctl', 'stop', 'virtualhere.service'], check=True)
                self.notification_label.config(text="Service stopped successfully.", fg="green")
            except subprocess.CalledProcessError:
                self.notification_label.config(text="Failed to stop service.", fg="red")

        # Clear the notification after 2 seconds
        self.notification_label.after(2000, lambda: self.notification_label.config(text="", fg="black"))

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

    def close_app(self, event):
        # Action to close the application gracefully
        self.root.destroy()

def main():
    root = tk.Tk()
    root.style = ttk.Style()
    root.style.configure("Toggle.TCheckbutton", background="#4CAF50", foreground="white", font=("Helvetica", 20, "bold"))

    app = VirtualHereToggleUI(root)

    # Set the application to start in fullscreen mode
    root.attributes("-fullscreen", True)

    root.mainloop()

if __name__ == "__main__":
    main()
