import logging
import docker
logger = logging.getLogger("docker")

class Docker:
    client : docker.DockerClient
    api : docker.APIClient
    default_registry : str

    def __init__(
        self,
        default_registry="localhost:5000",
        username="",
        password=""
    ):
        self.default_registry = default_registry
        self.username = username
        self.password = password
        self.init()
        
    def init(self):
        self.client = docker.from_env()
        self.api = docker.APIClient(base_url='unix://var/run/docker.sock')
        
    def connect(self):
        self.client.ping()
        
        # try to login to the default registry
        self.client.login(
            username=self.username,
            password=self.password,
            registry=self.default_registry
        )
        
        