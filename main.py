import os
import qrcode
from qrcode.image.pure import PyPNGImage
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform

class QRGenApp(App):
    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        Window.clearcolor = (1, 1, 1, 1)

        self.img = Image(size_hint=(1, 2), allow_stretch=True)
        self.status_label = Label(text="Enter URL below", color=(0.2, 0.2, 0.2, 1), size_hint=(1, 0.2))
        self.url_input = TextInput(hint_text="Type text or URL here", multiline=False, size_hint=(1, 0.3))
        
        self.gen_btn = Button(text="Generate QR", background_color=(0.2, 0.6, 1, 1), size_hint=(1, 0.3))
        self.gen_btn.bind(on_press=self.generate_qr)
        
        self.save_btn = Button(text="Save to Downloads", background_color=(0.2, 0.8, 0.2, 1), size_hint=(1, 0.3))
        self.save_btn.bind(on_press=self.save_qr)
        self.save_btn.disabled = True

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

        # Pure PNG factory completely bypasses Pillow requirements
        qr = qrcode.QRCode(box_size=10, border=4, image_factory=PyPNGImage)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image()
        
        # Save internally in private cache folder
        self.temp_path = os.path.join(self.user_data_dir, "temp_qr.png") if platform == 'android' else "temp_qr.png"
        
        with open(self.temp_path, "wb") as f:
            img.save(f)
        
        self.img.source = self.temp_path
        self.img.reload()
        self.status_label.text = "Generated! Ready to save."
        self.save_btn.disabled = False

    def save_qr(self, instance):
        try:
            download_path = "/storage/emulated/0/Download/my_qrcode.png" if platform == 'android' else "saved_qrcode.png"
            import shutil
            shutil.copyfile(self.temp_path, download_path)
            self.status_label.text = f"Saved to Downloads!"
        except Exception as e:
            self.status_label.text = "Error: Check Permissions"

if __name__ == '__main__':
    QRGenApp().run()
