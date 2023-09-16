import requests
import json

def get_scan(queue):
    while True:
        data = queue.get()
        if data != "":
            print(data)
            # Send the data to the Flask server
            response = requests.post("http://127.0.0.1:5999", data=json.dumps({"qr_code": data}))
        else:
            print("Scanner not connected")

@app.route('/qrcode', methods=['POST'])
def handle_qrcode():
    data = request.get_json()
    # Process the data...
    return jsonify({"message": "QR code processed successfully"}), 200
