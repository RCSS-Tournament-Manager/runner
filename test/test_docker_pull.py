from src.docker import Docker


async def run():
    docker_instance = Docker()
    docker_instance.connect()
    
    image_name = "nginx"
    image_tag = "latest"
    
    try:
        for output in docker_instance.pull_from_registry(
            image_name=image_name, 
            image_tag=image_tag,
            registry= "docker.io"
        ):
            print(output, end='')
        print("OK")
    except Exception as e:
        print(f"Failed to pull image: {e}")
