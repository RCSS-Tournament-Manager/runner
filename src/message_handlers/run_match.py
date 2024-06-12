from src.decorators import required_fields
from src.docker import Docker
from src.logger import get_logger
from src.rabbitmq import RabbitMQ
from src.storage import MinioClient
from src.utils.client_initializer import initialize_clients


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
    default_rabbit: RabbitMQ,
):
    ctx = config
    return ctx


logger = get_logger(__name__)

@required_fields(
    fields=[
        "match_id",
        "team_right",
        "team_right._type",
        "team_right.image",
        "team_right.team_name",
        "team_left",
        "team_left._type",
        "team_left.image",
        "team_left.team_name",
        "rcssserver",
        "rcssserver._type",
        "rcssserver.image",
    ]
)
async def run_match_command_handler(
    data: dict, docker: Docker, storage: MinioClient, reply, **kwargs
):
    # check the validation of the message
    match_id = data["match_id"]
    team_right_image = data["team_name"]
    image_name = data["image_name"]
    image_tag = data["image_tag"]

    file_id = data["file"]["file_id"]
    file_name = f"{file_id}.tar.gz"
    bucket = data["file"]["bucket"]

    tmp_folder = None
    tmp_file = None

    async def log_reply(message, log_fn=logger.info, e=None):
        log_fn(message)
        await reply(message)
        
    extracted_data, errors = initialize_clients(
        data, docker=docker, storage=storage, **kwargs
    )
    for error in errors:
        logger.error(error)
        await reply(error)
    # run the match
    # create tasks for streams

    pass
