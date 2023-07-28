#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import subprocess

# Function to check the status of the virtualhere service
def check_virtualhere_service():
    status_cmd = "systemctl is-active --quiet virtualhere.service"
    return subprocess.call(status_cmd, shell=True) == 0

# Function to toggle the virtualhere service
def toggle_virtualhere_service():
    action = "start" if not check_virtualhere_service() else "stop"
    cmd = f"sudo systemctl {action} virtualhere.service"
    subprocess.call(cmd, shell=True)
    messagebox.showinfo("VirtualHere Service", f"Service {action}ed")

# Create the Tkinter window
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg='white')

# Add a toggle button
toggle_button = tk.Button(root, text="Toggle VirtualHere Service", command=toggle_virtualhere_service)
toggle_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
