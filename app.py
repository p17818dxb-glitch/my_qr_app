import streamlit as st
import qrcode
from io import BytesIO

# Page Configuration
st.set_page_config(page_title="QR Code Generator", page_icon="📱", layout="centered")

# App Header
st.title("📱 Standalone QR Generator")
st.write("Enter your text or link below to instantly generate a scannable QR Code.")

# User Inputs
url_input = st.text_input("Enter URL or Text:", placeholder="https://example.com")
filename_input = st.text_input("Custom Save Filename:", value="my_qrcode.png")

if url_input:
    # Generate QR Code safely using pure Python logic
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url_input)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save Image to a Virtual Memory Buffer
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    # Display the QR Code on screen
    st.image(byte_im, caption="Your Generated QR Code", use_container_width=True)
    
    # Clean Download Button (Works natively on Android, iPhone, and PC)
    st.download_button(
        label="📥 Download QR Code to Device",
        data=byte_im,
        file_name=filename_input if filename_input.endswith(".png") else f"{filename_input}.png",
        mime="image/png"
    )
else:
    st.info("Waiting for input... Type something above to generate your QR Code.")
