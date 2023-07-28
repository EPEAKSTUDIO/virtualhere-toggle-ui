#!/bin/bash

# Remove the Python script
rm -f /tmp/virtualhere_service_gui.py

# Remove the autostart configuration
rm -f ~/.config/autostart/virtualhere_service_gui.desktop

# Prompt for confirmation before rebooting
read -p "Uninstallation complete. Do you want to restart your Raspberry Pi now? (Y/N): " choice
if [[ $choice =~ ^[Yy]$ ]]; then
  sudo reboot
else
  echo "You can manually reboot your Raspberry Pi to complete the uninstallation."
fi
