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
        """connect to docker
        """
        self.client.ping()
        
        self.client.login(
            username=self.username,
            password=self.password,
            registry=self.default_registry
        )
        
   
    
    def build_with_path(
        self, 
        path,
        image_name,
        image_tag,
        rm=False,
        timeout=12000
    ):
        """build an image with the given data

        Args:
            path (str): path to the folder with the Dockerfile
            image_name (str): name of the image
            image_tag (str): tag of the image
            rm (bool, optional): remove the image after building. Defaults to False.
            timeout (int, optional): timeout for the build. Defaults to 1200.
        """
        
        tag = f"{self.default_registry}/{image_name}:{image_tag}"
        build_progress = self.api.build(
            path=path,
            rm=rm,
            tag=tag,
            timeout=timeout,
        )
        for line in build_progress:
            yield line.decode('utf-8')          
    
        
    def push_to_registry(
        self,
        image_name,
        image_tag,
        registry=None,
    ):
        """push an image to the registry

        Args:
            image_name (str): name of the image
            image_tag (str): tag of the image
            registry (str): registry to push to
        """
        if registry is None:
            registry = self.default_registry
            
        push_progress = self.api.push(
            repository=f"{self.default_registry}/{image_name}",
            tag=image_tag,
            stream=True
        )
        for line in push_progress:
            yield line.decode('utf-8')
            
            
    def pull_from_registry(
        self,
        image_name,
        image_tag,
        registry=None,
    ):
        """pull an image from the registry

        Args:
            image_name (str): name of the image
            image_tag (str): tag of the image
            registry (str): registry to pull from
        """
        if registry is None:
            registry = self.default_registry
            
        pull_progress = self.api.pull(
            repository=f"{self.default_registry}/{image_name}",
            tag=image_tag,
            stream=True
        )
        for line in pull_progress:
            yield line.decode('utf-8')