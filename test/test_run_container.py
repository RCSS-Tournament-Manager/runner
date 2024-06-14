from src.docker import Docker
from src.logger import get_logger
import asyncio
from datetime import datetime

logger = get_logger(__name__)

async def read_log(container,docker_instance):
    last_read = datetime.now()
    container_id = container.id 
    while True:
        # read the logs
        # logs = container.logs(since=last_read,stdout=True,stderr=True,timestamps=True)
        # logs = logs.decode("utf-8")
        # # parse and seprate each line 
        # logs = logs.split("\n")
        # for log in logs:
        #     if log:
        #         logger.info(f"+ {log}")
        # # print(f"+ {logs}")
        # last_read = datetime.now()
        
        # https://stackoverflow.com/questions/67650841/how-to-find-memory-usage-with-memory-profiler-python
         
        
        
        logs = docker_instance.api.logs(container=container_id,stdout=True,stderr=True,timestamps=True, since=last_read)
        logs = logs.decode("utf-8")
        logs = logs.split("\n")
        for log in logs:
            if log:
                logger.info(f"+ {log}")
        
        # print('\n\n\n')
        # last_read must be UNIX timestamp for the logs staring point. like 
        last_read = datetime.now().timestamp()
        
        await asyncio.sleep(1)
    # pass

async def run():
    docker_instance = Docker()
    docker_instance.connect()
    
    # Pull the nginx image from Docker Hub
    for line in docker_instance.pull_from_registry("nginx", "latest", registry="docker.io"):
        logger.info(line)
    
    container = docker_instance.run_container(
        image_name="nginx",
        image_tag="latest",
        command=None,
        registry="docker.io",
        ports={'80/tcp': 8080},
        network="team-builder-dev_network",
        name="nginx_test_container",
    )
    # create task to read logs
    task = asyncio.create_task(read_log(container,docker_instance))
    
    await asyncio.sleep(10)
    
    # Now kill the container and log its exit code
    logger.info(f"Now we kill the container")
    docker_instance.kill_container(container=container)
    logger.info(f"Container exited")
    return
