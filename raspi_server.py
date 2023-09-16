from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Lock

"""
Background Thread
"""
barcode_thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config["SECRET_KEY"] = "donsky!"
socketio = SocketIO(app, cors_allowed_origins="*")


class ServerClass:
    dustbinLevel = 0
    currentUser = None

    def currentUserAvailable():
        return ServerClass.currentUser is not None

    def updateCurrentUser(user):
        ServerClass.currentUser = user

    def removeCurrentUser():
        ServerClass.currentUser = None

    def updateDustbinLevel():
        pass


def barcode_thread():
    while True:
        result = str(input())
        print(result)
        if ServerClass.currentUser == result:
            print("Logged out")
            payload = {
                "id": result,
                "action": "logout",
            }
            socketio.emit("useraction", payload)
            socketio.sleep(1)
            ServerClass.removeCurrentUser()

        elif ServerClass.currentUser is None:
            print("Logged in")
            payload = {
                "id": result,
                "action": "login",
            }
            socketio.emit("useraction", payload)
            socketio.sleep(1)
            ServerClass.updateCurrentUser(result)

        else:
            print("An user is already logged in")
            payload = {
                "id": result,
                "action": "duplicate_login",
            }
            socketio.emit("useraction", payload)
            socketio.sleep(1)


"""
Serve root index file
"""


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/qrcode', methods=['POST'])
def handle_qrcode():
    data = request.get_json()
    # Process the data...
    return jsonify({"message": "QR code processed successfully"}), 200




"""
Decorator for connect
"""


@socketio.on("connect")
def connect():
    global barcode_thread
    print("Client connected")

    global barcode_thread
    with thread_lock:
        if barcode_thread is None:
            barcode_thread = socketio.start_background_task(barcode_thread)


"""
Decorator for disconnect
"""


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected", request.sid)


if __name__ == "__main__":
    socketio.run(app, port=5999)



