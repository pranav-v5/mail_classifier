from core.env_server import create_fastapi_app
from .environment import EmailEnvironment

env = EmailEnvironment()
app = create_fastapi_app(env)
