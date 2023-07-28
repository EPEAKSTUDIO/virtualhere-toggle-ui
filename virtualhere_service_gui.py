import tkinter as tk
from tkinter import ttk
import subprocess

class VirtualHereToggleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VirtualHere Toggle UI")
        self.root.geometry("800x480")  # Set the window size to 800x480 (16:9 ratio)
        self.root.attributes("-fullscreen", True)  # Open in fullscreen mode

        # Create the toggle button (large 16:9 ratio tile)
        self.toggle_var = tk.BooleanVar()
        self.toggle_button = tk.Button(
            self.root,
            text="USB over IP",
            variable=self.toggle_var,
            command=self.on_toggle_change,
            font=("Helvetica", 30, "bold"),
            relief="flat",
            borderwidth=0,
            background="#4CAF50",  # Green color
            foreground="white"  # White text color
        )
        self.toggle_button.place(relx=0.5, rely=0.5, anchor="center")

        # Create the text notification label (initially empty)
        self.notification_label = ttk.Label(
            self.root,
            text="",
            font=("Helvetica", 16)
        )
        self.notification_label.place(relx=0.5, rely=0.95, anchor="s")  # Display below the button

        # Bind the close event to the root
        self.root.bind("<Escape>", self.close_app)

        # Set the initial position of the toggle based on the service status
        self.set_initial_toggle_position()

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

        self.toggle_button.config(background="#4CAF50" if self.toggle_var.get() else "red")

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
        self.toggle_button.config(background="#4CAF50" if initial_status else "red")

    def close_app(self, event):
        # Action to close the application gracefully
        self.root.destroy()

def main():
    root = tk.Tk()

    app = VirtualHereToggleUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
