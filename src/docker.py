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
        if registry == None:
            registry = self.default_registry
            
        pull_progress = self.api.pull(
            repository=f"{registry}/{image_name}",
            tag=image_tag,
            stream=True
        )
        for line in pull_progress:
            yield line.decode('utf-8')
            
             
    def run_container(
        self,
        image_name,
        image_tag,
        command,
        detach=True,
        remove=True,
        registry=None,
        **kwargs
    ):
        """run a container

        Args:
            image_name (str): name of the image
            image_tag (str): tag of the image
            command (str): command to run in the container
            detach (bool, optional): run the container in the background. Defaults to True.
            remove (bool, optional): remove the container after it stops. Defaults to True.
        """
        if registry == None:
            registry = self.default_registry
        container = self.client.containers.run(
            image=f"{registry}/{image_name}:{image_tag}",
            command=command,
            detach=detach,
            remove=remove,
            **kwargs
        )
        return container


    def run_and_log_container(
        self,
        image_name,
        image_tag,
        command,
        registry=None,
        **kwargs
    ):
        """run a container in detached mode and print its logs

        Args:
            image_name (str): name of the image
            image_tag (str): tag of the image
            command (str): command to run in the container
            registry (str, optional): registry to pull from. Defaults to None.
        """
        if registry is None:
            registry = self.default_registry
        
        container = self.client.containers.run(
            image=f"{registry}/{image_name}:{image_tag}",
            command=command,
            detach=True,
            **kwargs
        )
        yield container
        
        for log in container.logs(stream=True):
            yield log.decode('utf-8')
        

    def stop_container(
        self,
        container=None,
        container_id=None,
        container_name=None
    ):
        """Stop a running container

        Args:
            container_id (str, optional): ID of the container to stop. Defaults to None.
            container_name (str, optional): Name of the container to stop. Defaults to None.
        
        Returns:
            bool: True if the container was stopped successfully, False otherwise.
        """
        try:
            if container == None:
                if container_id:
                    container = self.client.containers.get(container_id)
                elif container_name:
                    container = self.client.containers.get(container_name)
            
            if container:
                container.stop()
                return True

            logger.error("Container not found")
            return False
        except Exception as e:
            logger.error(f"Error stopping container: {e}")
            return False

    def kill_container(
        self,
        container=None,
        container_id=None,
        container_name=None
    ):
        """Kill a running container

        Args:
            container_id (str, optional): ID of the container to kill. Defaults to None.
            container_name (str, optional): Name of the container to kill. Defaults to None.
        
        Returns:
            bool: True if the container was killed successfully, False otherwise.
        """
        try:
            if container == None:
                if container_id:
                    container = self.client.containers.get(container_id)
                elif container_name:
                    container = self.client.containers.get(container_name)
                    
                    
            if container:
                container.kill()
                return True
            
            logger.error("Container not found")
            return False
        except Exception as e:
            logger.error(f"Error killing container: {e}")
            return False
        
    def rm_container(
        self,
        container=None,
        container_id=None,
        container_name=None
    ):
        """Remove a container

        Args:
            container_id (str, optional): ID of the container to remove. Defaults to None.
            container_name (str, optional): Name of the container to remove. Defaults to None.
        
        Returns:
            bool: True if the container was removed successfully, False otherwise.
        """
        try:
            if container == None:
                if container_id:
                    container = self.client.containers.get(container_id)
                elif container_name:
                    container = self.client.containers.get(container_name)
            
            if container:
                container.remove()
                return True
            
            logger.error("Container not found")
            return False
        except Exception as e:
            logger.error(f"Error removing container: {e}")
            return False