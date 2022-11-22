import urllib.request
import socketio
import time
# Install request websocket-client

with urllib.request.urlopen("http://127.0.0.1:8000/") as response:
	print(response.read())

client = socketio.Client()

client.connect("http://127.0.0.1:8000")
time.sleep(1)
client.disconnect()