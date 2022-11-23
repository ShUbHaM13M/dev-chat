import uvicorn
from fastapi import FastAPI, Request
import socketio

sio = socketio.AsyncServer(async_mode="asgi")
socket_app = socketio.ASGIApp(sio)
app = FastAPI()

@app.get('/')
async def test():
	return {"message": "works"}

@app.route('/login')
async def login(request: Request):
	pass

app.mount('/', socket_app)

@sio.on("connect")
async def on_connect(sid, env):
	print(f'{sid} connected')

@sio.on("disconnect")
async def on_disconnect(sid):
	print(f'{sid} disconnected')

if __name__ == '__main__':
	uvicorn.run('app:app', reload=True, host="192.168.0.105", port=8000)