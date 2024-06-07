from src.docker import Docker
from src.rabbitmq import RabbitMQ
from src.storage import MinioClient


async def run_team_docker(
    player_prefix: str,
    team_left_image_name: str,
    core_start: int,
    core_end: int,
    docker_i: Docker,
):
    pass


async def run_server_docker(
    server_image_name: str, core_start: int, core_end: int, docker_i: Docker
):
    pass


async def config_validator(config: dict):
    client_parsed = []
    return client_parsed


async def add_client_to_external_connections(
    config: dict,
    client_parsed: list, 
    default_docker: Docker,
    defult_storage: MinioClient,
    default_rabbit: RabbitMQ
):
    ctx = config
    return ctx





async def run_match_command_handler(data: dict, **kwargs):
    # check the validation of the message
    # loop trough all the keys in the message and add "client" field to external connections
    # if the external connection is not available, create the connection class and put it on client field
    # run the match
    # create tasks for streams
    pass
