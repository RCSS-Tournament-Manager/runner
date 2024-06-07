import os
from src.docker import Docker
from dotenv import load_dotenv

load_dotenv()

HOST = os.environ.get('HOST')
PORT = int(os.environ.get('PORT'))
DOCKER_REGISTRY=os.environ.get('DOCKER_REGISTRY')


docker_i: Docker = None