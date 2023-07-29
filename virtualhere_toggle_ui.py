from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
import subprocess

class VirtualHereToggleUI(App):
    def build(self):
        Window.fullscreen = True
        layout = BoxLayout(orientation='vertical')
        toggle_button = ToggleButton(text="USB over IP", font_size=40, size_hint=(1, 0.7))
        toggle_button.bind(on_press=self.on_toggle_change)
        self.notification_label = Label(text="", font_size=20, size_hint=(1, 0.3))
        layout.add_widget(toggle_button)
        layout.add_widget(self.notification_label)
        self.set_initial_toggle_position()  # Add your logic to determine the initial status
        return layout

    def on_toggle_change(self, instance):
        self.toggle_var = instance.state == 'down'
        self.update_toggle_color()

        if self.toggle_var:
            self.notification_label.text = "Starting service..."
            try:
                subprocess.run(['sudo', 'systemctl', 'start', 'virtualhere.service'], check=True)
                self.notification_label.text = "Service started successfully."
                self.set_initial_toggle_position()
            except subprocess.CalledProcessError:
                self.notification_label.text = "Failed to start service."
                instance.state = 'normal'
        else:
            self.notification_label.text = "Stopping service..."
            try:
                subprocess.run(['sudo', 'systemctl', 'stop', 'virtualhere.service'], check=True)
                self.notification_label.text = "Service stopped successfully."
                self.set_initial_toggle_position()
            except subprocess.CalledProcessError:
                self.notification_label.text = "Failed to stop service."
                instance.state = 'down'

    def set_initial_toggle_position(self):
        # Get the initial status of the service from systemctl
        try:
            result = subprocess.run(['systemctl', 'is-active', 'virtualhere.service'], capture_output=True, text=True, check=True)
            initial_status = (result.stdout.strip() == "active")
        except subprocess.CalledProcessError:
            # In case of an error (e.g., service not found), assume the service is inactive
            initial_status = False

        self.toggle_var = initial_status
        self.update_toggle_color()

    def update_toggle_color(self):
        if self.toggle_var:
            self.notification_label.color = (0, 1, 0, 1)  # Green
        else:
            self.notification_label.color = (1, 0, 0, 1)  # Red

if __name__ == "__main__":
    VirtualHereToggleUI().run()
