import os
from src.docker import Docker
from dotenv import load_dotenv

load_dotenv()

HOST = os.environ.get('HOST')
PORT = int(os.environ.get('PORT'))
DOCKER_REGISTRY=os.environ.get('DOCKER_REGISTRY')

#RabbitMQ Variables
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
RABBITMQ_ADDRESS = os.environ.get('RABBITMQ_ADDRESS')
RabbitMQ_PORT = int(os.environ.get('RabbitMQ_PORT'))

#Docker registery variables
DOCKER_REGISTERY_USERNAME = os.environ.get('DOCKER_REGISTERY_USERNAME')
DOCKER_REGISTERY_PASSWORD = os.environ.get('DOCKER_REGISTERY_PASSWORD')
DOCKER_REGISTERY_ADDRESS = os.environ.get('DOCKER_REGISTERY_ADDRESS')
DOCKER_REGISTERY_PORT = int(os.environ.get('DOCKER_REGISTERY_PORT'))

#MINIO variables
MINIO_USERNAME = os.environ.get('MINIO_USERNAME')
MINIO_PASSWORD = os.environ.get('MINIO_PASSWORD')
MINIO_ADDRESS = os.environ.get('MINIO_ADDRESS')
MINIO_PORT = int(os.environ.get('MINIO_PORT'))

#WEBSERVER variables 
WEBSERVER_ADDRESS = os.environ.get('WEBSERVER_ADDRESS')
WEBSERVER_PORT = int(os.environ.get('WEBSERVER_PORT'))

#Extra
DOCKER_FILE_DIR = os.environ.get('DOCKER_FILE_DIR')
DOCKER_FILE_NAME = os.environ.get('DOCKER_FILE_NAME')

DEFAULT_UPLOAD_FOLDER_DIR = os.environ.get('DEFAULT_UPLOAD_FOLDER_DIR')
DEFAULT_UPLOAD_FOLDER_NAME = os.environ.get('DEFAULT_UPLOAD_FOLDER_NAME')


DEFAULT_TEAM_BUILD_DOCKERFILE = os.path.join(
    os.path.dirname(__file__), 
    DOCKER_FILE_DIR, 
    DOCKER_FILE_NAME
)

DEFAULT_UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__), 
    DEFAULT_UPLOAD_FOLDER_DIR,
    DEFAULT_UPLOAD_FOLDER_NAME
)

USE_TMP_UPLOAD_FOLDER = False

REMOVE_AFTER_BUILD = False

docker_i: Docker = None