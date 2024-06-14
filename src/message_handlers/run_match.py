from src.decorators import required_fields
from src.docker import Docker
from src.logger import get_logger
from src.rabbitmq import RabbitMQ
from src.storage import MinioClient
from src.utils.client_initializer import initialize_clients
from datetime import datetime
import asyncio

logger = get_logger(__name__)



@required_fields(
    fields=[
        "match_id",
        "team_right",
        "team_right._type",
        "team_right.image_name",
        "team_right.team_name",
        "team_left",
        "team_left._type",
        "team_left.image_name",
        "team_left.team_name",
        "rcssserver",
        "rcssserver._type",
        "rcssserver.image_name",
    ]
)
async def run_match_command_handler(
    data: dict, docker: Docker, storage: MinioClient, reply, **kwargs
):
    # check the validation of the message
    match_id = data["match_id"]

    async def log_reply(message, log_fn=logger.info, e=None):
        if e:
            log_fn(f"{message}: {e}")
        else:
            log_fn(message)
        await reply(message)


    extracted_data, errors = initialize_clients(
        data, docker=docker, storage=storage, **kwargs
    )
    for error in errors:
        await log_reply(error, logger.error)
    
    d = extracted_data
    # ----------------------------------
    # pull images
    # ----------------------------------
    
    # ----- pull team right image
    try:
        tr = d["team_right"]
        client = d["team_right"]["_client"]
        for output in client.pull_from_registry(
            image_name=tr["image_name"],
            image_tag=tr["tag"],
        ):
            await log_reply(output, logger.info)
    except Exception as e:
        await log_reply(f"Failed to pull right team image", logger.error, e)
        return

    # ----- pull team left image
    try:
        tl = d["team_left"]
        client = d["team_left"]["_client"]
        for output in client.pull_from_registry(
            image_name=tl["image_name"],
            image_tag=tl["tag"],
        ):
            await log_reply(output, logger.info)
    except Exception as e:
        await log_reply(f"Failed to pull left team image", logger.error, e)
        return

    # ----- pull rcssserver image
    try:
        rcss = d["rcssserver"]
        client = d["rcssserver"]["_client"]
        for output in client.pull_from_registry(
            image_name=rcss["image_name"],
            image_tag=rcss["tag"],
        ):
            await log_reply(output, logger.info)
    except Exception as e:
        await log_reply(f"Failed to pull rcssserver image", logger.error, e)
        return
    
    # ----------------------------------
    # run server
    # ----------------------------------
    
    await log_reply("Starting rcssserver...")
    
     
       
    async def read_server_log(container, docker_instance, event):
        last_read = datetime.now()
        container_id = container.id 
        while True:
            try:
                logs = docker_instance.api.logs(container=container_id, stdout=True, stderr=True, timestamps=True , since = last_read)
                logs = logs.decode("utf-8")
                import re
                all = re.findall(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z", logs)
                if all:
                    for i in range(len(all)):
                        if datetime.fromisoformat(all[i]) > last_read:
                            last_read = all[i]
                    

                logs = logs.split("\n")
                
                for log in logs:
                    if log:
                        # find all timestamp with regex the last one is the most recent
                        await log_reply(f"{log}")
                        if "Using simulator's random seed as Hetero Player Seed:" in log:
                            event.set()
                await asyncio.sleep(1)
            except Exception as e:
                await log_reply("Failed to read server logs", logger.error, e)
                await asyncio.sleep(50)
    
    tcp_port = 6000

    try:
        # create container
        server_container = d["rcssserver"]["_client"].run_container(
            image_name=d["rcssserver"]["image_name"],
            image_tag=d["rcssserver"]["tag"],
            command=None,
            ports={f'{tcp_port}/tcp': tcp_port},
            network="team-builder-dev_network",
            name="rcss_server_test",
        )
        
    except Exception as e:
        await log_reply("Failed to run rcssserver ", logger.error, e)
        return
    
    event = asyncio.Event()
    read_server_task = asyncio.create_task(read_server_log(server_container, d["rcssserver"]["_client"], event))
    
    # wait until the specific log message is found
    await event.wait()
    
    await log_reply("rcssserver is ready")


    # ----------------------------------
    server_ip = server_container.attrs["NetworkSettings"]["IPAddress"]
    logger.info(f"Server IP: {server_ip}")
    
    for i in range(11):
        try:
            # create container
            container = d["team_right"]["_client"].run_container(
                image_name=d["team_right"]["image_name"],
                image_tag=d["team_right"]["tag"],
                command=None,
                network="team-builder-dev_network",
                name=f"{d["team_right"]["team_name"]}_{i}",
                log_config=None,
                environment={"num": i, "ip": server_ip},
            )
            await log_reply(f"team_right_{i} container created")
        except Exception as e:
            await log_reply("Failed to connect right team", logger.error, e)
            return
    for i in range(11):
        try:
            # create container
            container = d["team_left"]["_client"].run_container(
                image_name=d["team_left"]["image_name"],
                image_tag=d["team_left"]["tag"],
                command=None,
                network="team-builder-dev_network",
                name=f"{d["team_left"]["team_name"]}_{i}",
                environment={"num": i, "ip": server_ip},
                log_config=None,
            )
            await log_reply(f"team_left_{i} container created")
        except Exception as e:
            await log_reply("Failed to connect left team", logger.error, e)
            return
    
    # create tasks for streams
    await asyncio.sleep(5000)
    pass
