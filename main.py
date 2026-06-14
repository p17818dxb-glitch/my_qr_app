import os
import qrcode
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform
from android.permissions import request_permissions, Permission # type: ignore

class QRGenApp(App):
    def build(self):
        # 1. Ask for storage permissions on startup (Android only)
        if platform == 'android':
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

        # 2. Main Layout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        Window.clearcolor = (1, 1, 1, 1)  # White background

        # 3. Widgets
        self.img = Image(source='icon.png', size_hint=(1, 2), allow_stretch=True) # Placeholder
        self.status_label = Label(text="Enter URL below", color=(0.2, 0.2, 0.2, 1), size_hint=(1, 0.2))
        self.url_input = TextInput(hint_text="Type text or URL here", multiline=False, size_hint=(1, 0.3))
        
        self.gen_btn = Button(text="Generate QR", background_color=(0.2, 0.6, 1, 1), size_hint=(1, 0.3))
        self.gen_btn.bind(on_press=self.generate_qr)
        
        self.save_btn = Button(text="Save to Downloads", background_color=(0.2, 0.8, 0.2, 1), size_hint=(1, 0.3))
        self.save_btn.bind(on_press=self.save_qr)
        self.save_btn.disabled = True

        # 4. Add widgets to layout
        self.layout.add_widget(self.img)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.url_input)
        self.layout.add_widget(self.gen_btn)
        self.layout.add_widget(self.save_btn)
        
        return self.layout

    def generate_qr(self, instance):
        text = self.url_input.text.strip()
        if not text:
            self.status_label.text = "Please enter text first!"
            return

        # Generate QR
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save temp file for display
        self.temp_path = "temp_qr.png"
        img.save(self.temp_path)
        
        # Update Image Widget
        self.img.source = self.temp_path
        self.img.reload()
        self.status_label.text = "Generated! Ready to save."
        self.save_btn.disabled = False

    def save_qr(self, instance):
        try:
            # Android-specific path to Downloads folder
            download_path = "/storage/emulated/0/Download/my_qrcode.png"
            
            # If on PC (testing), save to current folder
            if platform != 'android':
                download_path = "saved_qrcode.png"

            from shutil import copyfile
            copyfile(self.temp_path, download_path)
            self.status_label.text = f"Saved to:\n{download_path}"
        except Exception as e:
            self.status_label.text = "Error: Check Permissions"

if __name__ == '__main__':
    QRGenApp().run()
