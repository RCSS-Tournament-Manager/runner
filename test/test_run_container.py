from src.docker import Docker
from src.logger import get_logger
import asyncio
from datetime import datetime
import re

logger = get_logger(__name__)

async def read_log(container, docker_instance):
    container_id = container.id 
    since = datetime.now().timestamp()
    while True:
        await asyncio.sleep(1)
        until = datetime.now().timestamp()
        logs = docker_instance.api.logs(
            container=container_id,
            stdout=True,
            stderr=True,
            timestamps=True, 
            since=since,
            until=until
        )
        since = until  # Update 'since' to the 'until' timestamp
        logs = logs.decode("utf-8")
        logs = logs.split("\n")
        for log in logs:
            if log:
                logger.info(f"+ {log}")
        
        last_read = datetime.now().timestamp()

async def run():
    docker_instance = Docker()
    docker_instance.connect()
    server_tcp_port = 6000
    
    # Pull the nginx image from Docker Hub
    for line in docker_instance.pull_from_registry("rcssserver", "latest"):
        logger.info(line)
    
    container = docker_instance.run_container(
        image_name="rcssserver",
        image_tag="latest",
        ports={f'{server_tcp_port}/tcp': server_tcp_port},
        network="team-builder-dev_network",
        name="nginx_test_container",
    )
    # create task to read logs
    task = asyncio.create_task(read_log(container, docker_instance))
    
    await asyncio.sleep(100)
    
    # Now kill the container and log its exit code
    logger.info(f"Now we kill the container")
    docker_instance.kill_container(container=container)
    logger.info(f"Container exited")
    return