import tkinter as tk
from tkinter import ttk
import subprocess

class VirtualHereToggleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VirtualHere Toggle UI")
        self.root.attributes("-fullscreen", True)  # Open in fullscreen mode

        # Create a frame to hold the toggle and notifications at the center of the screen
        center_frame = ttk.Frame(self.root)
        center_frame.pack(expand=True)

        # Configure the vertical space to take about 70% of the screen's height
        center_frame.grid_rowconfigure(0, weight=7)
        center_frame.grid_rowconfigure(1, weight=3)

        # Create the on/off toggle button (large 16:9 ratio rectangle)
        self.toggle_var = tk.BooleanVar()
        self.toggle_button = tk.Button(
            center_frame,
            text="USB over IP",
            variable=self.toggle_var,
            command=self.on_toggle_change,
            font=("Helvetica", 20),
            relief="flat",
            borderwidth=0
        )
        self.toggle_button.pack(expand=True, fill=tk.BOTH)
        self.toggle_var.trace_add('write', self.update_toggle_color)  # Update the toggle color when the status changes

        # Create the text notification label (initially empty)
        self.notification_label = ttk.Label(
            center_frame,
            text="",
            font=("Helvetica", 12)
        )
        self.notification_label.pack(expand=True)

        # Create the close button (red cross) top right
        close_btn = tk.Label(
            self.root,
            text="X",
            font=("Helvetica", 12, "bold"),
            fg="red",
            cursor="hand2"
        )
        close_btn.place(x=self.root.winfo_screenwidth()-25, y=0, anchor="ne")
        close_btn.bind("<Button-1>", self.close_app)

        # Set the initial position of the toggle based on the service status
        self.set_initial_toggle_position()

    def on_toggle_change(self, *_):
        # Handle the action when the toggle is switched on/off
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

        self.toggle_button.config(text="USB over IP")  # Always show "USB over IP" on the button
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
        self.toggle_button.config(text="USB over IP", fg="green" if initial_status else "red")

    def update_toggle_color(self, *_):
        # Update the toggle color based on the status
        self.toggle_button.config(fg="green" if self.toggle_var.get() else "red")

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
