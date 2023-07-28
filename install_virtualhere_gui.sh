#!/bin/bash

# Install Python and Tkinter
sudo apt update
sudo apt install -y python3 python3-tk

# Download the Python script from your GitHub repository
wget -O /tmp/virtualhere_service_gui.py https://raw.githubusercontent.com/your-username/your-repo/main/virtualhere_service_gui.py

# Configure the script to start on boot
cat <<EOF | sudo tee ~/.config/autostart/virtualhere_service_gui.desktop > /dev/null
[Desktop Entry]
Name=VirtualHere Service GUI
Type=Application
Exec=/usr/bin/python3 /tmp/virtualhere_service_gui.py
EOF

# Make the script executable
chmod +x /tmp/virtualhere_service_gui.py

# Reboot to start the script automatically on boot
sudo reboot
