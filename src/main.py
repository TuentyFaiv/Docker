from flask import Flask
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app)
socket = SocketIO(app, cors_allowed_origins="*")

@app.get("/")
def handle_home():
  return "Hello world"

@socket.on("connect")
def handle_connect(auth):
  print("Client connected")
  emit("connected user", { "data" : "Connected" })

@socket.on("disconnect")
def handle_disconnect():
  print("Client disconnected")

@socket.on("message")
def handle_message(msg):
  send(msg, broadcast=True)

@socket.on("remove_message")
def handle_message(id):
  send(id, broadcast=True)

if __name__ == "__main__":
  socket.run(app, debug=True, port="4000", host="0.0.0.0")
