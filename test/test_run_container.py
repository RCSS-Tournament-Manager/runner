from src.docker import Docker
from src.logger import get_logger
import asyncio
import concurrent.futures

logger = get_logger(__name__)

def log_container(container):
    """Logs the output of a running container."""
    try:
        for log in container.logs(stream=True):
            print(f'+ {log.decode("utf-8")}')
    except asyncio.CancelledError:
        print("Logging task has been cancelled")
        raise

async def run():
    docker_instance = Docker()
    docker_instance.connect()
    
    # Pull the nginx image from Docker Hub
    for line in docker_instance.pull_from_registry("nginx", "latest", registry="docker.io"):
        logger.info(line)
    
    # Run the nginx container and log its output
    container = docker_instance.run_container(
        image_name="nginx",
        image_tag="latest",
        command="nginx -g 'daemon off;'",
        registry="docker.io",
        ports={'80/tcp': 8080},
        network="team-builder-dev_network",
        name="nginx_test_container"
    )
    loop = asyncio.get_event_loop()
    
    # Use run_in_executor to run the blocking function in a separate thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        t2 = loop.create_task(loop.run_in_executor(executor, log_container, container))
    # Start a separate task to log the container's output

    # Wait for 10 seconds and then cancel the logging task
    logger.info(f"Waiting for 10 seconds before cancelling the logging task")
    await asyncio.sleep(10)
    t2.cancel()

    try:
        await t2
    except asyncio.CancelledError:
        pass

    # Now kill the container and log its exit code
    logger.info(f"Now we kill the container")
    docker_instance.kill_container(container=container)
    logger.info(f"Container exited")
    return