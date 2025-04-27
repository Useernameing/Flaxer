from flask import Flask, jsonify, render_template, request
import cv2
import os
import time
import threading
from datetime import datetime
import sys

app = Flask(__name__)

is_capture_running = False
capture_thread = None
capture_directory = "captured_images"

if not os.path.exists(capture_directory):
    os.makedirs(capture_directory)

def clear_terminal():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def capture_images():
    global is_capture_running
    Flazerx = cv2.VideoCapture(0)

    if not Flazerx.isOpened():
        print("Flazerx açılmadı!")
        return

    image_count = 0

    while is_capture_running:
        ret, frame = Flazerx.read()

        if ret:
            image_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = os.path.join(capture_directory, f"flazerx_{timestamp}.jpg")
            try:
                cv2.imwrite(image_filename, frame)
                print(f"Flazerx {image_filename} kaydedildi.")
            except Exception as e:
                print(f"Resim kaydedilirken hata oluştu: {e}")
            time.sleep(0.5)

    Flazerx.release()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_capture():
    global is_capture_running, capture_thread

    if is_capture_running:
        return jsonify({"message": "Flazerx çekme işlemi zaten devam ediyor!"}), 400

    clear_terminal()
    print("\033[1;35mFlazerX Sunucusu Başlatıldı!\033[0m")

    is_capture_running = True
    capture_thread = threading.Thread(target=capture_images)
    capture_thread.start()

    return jsonify({"message": "Flazerx çekme işlemi başlatıldı!"})

@app.route('/stop', methods=['GET'])
def stop_capture():
    global is_capture_running

    if not is_capture_running:
        return jsonify({"message": "Flazerx çekme işlemi zaten durdurulmuş!"}), 400

    is_capture_running = False
    capture_thread.join()

    saved_path = os.path.abspath(capture_directory)
    return jsonify({"message": f"Flazerx çekme işlemi durduruldu! Flazerx'ler şu dizine kaydedildi: {saved_path}",
                    "last_image_path": os.path.join(saved_path, f"flazerx_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")})

@app.route('/set_Flazerx', methods=['POST'])
def set_Flazerx():
    return jsonify({"message": "Flazerx seçimi başarıyla yapıldı!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
