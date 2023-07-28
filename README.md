# VirtualHere Toggle UI

This repository contains a Python script that creates a simple GUI with a toggle button to show and control the status of the "virtualhere.service" on a Raspberry Pi. The script utilizes Tkinter for the graphical user interface and interacts with the "systemctl" command to manage the service.

## Installation

To install and run the VirtualHere Toggle UI on your Raspberry Pi, download and run the installer script using `curl | bash`:

```bash
curl -sSL https://raw.githubusercontent.com/EPEAKSTUDIO/virtualhere-toggle-ui/main/install_virtualhere_gui.sh | bash


The installer script will take care of setting up the necessary configurations and dependencies. After the installation is complete, your Raspberry Pi will reboot, and the VirtualHere Toggle UI will start automatically on boot, providing a touchscreen interface to control the "virtualhere.service" status.

## Usage
Once the installation is complete, the VirtualHere Toggle UI will automatically start on boot. The UI displays a toggle button that represents the status of the "virtualhere.service." You can use the touchscreen interface to start or stop the service by tapping the button.

## License
This project is licensed under the MIT License.