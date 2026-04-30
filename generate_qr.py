import qrcode
import os
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Use a dummy IP to get local interface IP
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def generate_exam_qr(token):
    local_ip = get_local_ip()
    base_url = f"http://{local_ip}:5001"
    
    # Create the link
    link = f"{base_url}/?exam_token={token}"
    print(f"Generating QR for: {link}")
    
    # Generate QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save image
    output_path = "data/exam_qr.png"
    img.save(output_path)
    print(f"QR Code saved to: {os.path.abspath(output_path)}")
    print(f"\nIMPORTANT: Your phone must be on the same Wi-Fi as your laptop ({local_ip})")

if __name__ == "__main__":
    generate_exam_qr("QUIZ-2026-TEST")
