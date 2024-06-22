from src.decorators import required_fields
from src.docker import Docker
from src.logger import get_logger
from src.rabbitmq import RabbitMQ
from src.states import StateManager
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
    data: dict, 
    docker: Docker, 
    storage: MinioClient, 
    state_manager: StateManager,
    reply, 
    **kwargs
):
    # check the validation of the message
    match_id = data["match_id"]
    
    network_name ="team-builder-dev_network"
    server_tcp_port = 6000

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
        container_id = container.id 
        since = datetime.now().timestamp()
        while True:
            try:
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
                        # Check for specific log message to set the event
                        if "Using simulator's random seed as Hetero Player Seed:" in log:
                            event.set()
            except Exception as e:
                logger.error("Failed to read server logs", exc_info=e)
                await asyncio.sleep(50)

    try:
        # create container
        server_container = d["rcssserver"]["_client"].run_container(
            image_name=d["rcssserver"]["image_name"],
            image_tag=d["rcssserver"]["tag"],
            command=None,
            ports={f'{server_tcp_port}/tcp': server_tcp_port},
            network=network_name,
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
    container_info = d["rcssserver"]["_client"].api.inspect_container(server_container.id)
    server_ip = container_info["NetworkSettings"]["Networks"][network_name]["IPAddress"]
    logger.info(f"Server IP: {server_ip}")
    
    
    for i in range(11):
        try:
            # create container
            container = d["team_right"]["_client"].run_container(
                image_name=d["team_right"]["image_name"],
                image_tag=d["team_right"]["tag"],
                network=network_name,
                name=f"r_{d["team_right"]["team_name"]}_{i}",
                environment={"num": i, "ip": server_ip},
                log_config=None
            )
            await log_reply(f"team_right_{i} container created")
            asyncio.sleep(1)
        except Exception as e:
            await log_reply("Failed to connect right team", logger.error, e)
            return
        
    for i in range(11):
        try:
            # create container
            container = d["team_left"]["_client"].run_container(
                image_name=d["team_left"]["image_name"],
                image_tag=d["team_left"]["tag"],
                network=network_name,
                name=f"l_{d["team_left"]["team_name"]}_{i}",
                environment={"num": i, "ip": server_ip},
                log_config=None
            )
            await log_reply(f"team_left_{i} container created")
            asyncio.sleep(1)
        except Exception as e:
            await log_reply("Failed to connect left team", logger.error, e)
            return
    
    # create tasks for streams
    await asyncio.sleep(5000)
    pass
