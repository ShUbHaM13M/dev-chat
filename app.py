import uvicorn
from fastapi import FastAPI, Request
import socketio
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

config = Config('.env')
oauth = OAuth(config)
oauth.register(
	name = "google",
	server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
	client_kwargs = {
		'scope': 'openid email profile'
	}
)

sio = socketio.AsyncServer(async_mode="asgi")
socket_app = socketio.ASGIApp(sio)
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret")

@app.get('/')
async def test():
	return {"message": "works"}

@app.route('/login')
async def login(request: Request):
	redirect_uri = request.url_for('auth')
	return await oauth.google.authorize_redirect(request, redirect_uri)

app.mount('/', socket_app)

@sio.on("connect")
async def on_connect(sid, env):
	print(f'{sid} connected')

@sio.on("disconnect")
async def on_disconnect(sid):
	print(f'{sid} disconnected')

if __name__ == '__main__':
	uvicorn.run('app:app', reload=True)