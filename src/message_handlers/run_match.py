from src.decorators import required_fields
from src.docker import Docker
from src.logger import get_logger
from src.rabbitmq import RabbitMQ
from src.storage import MinioClient
from src.utils.client_initializer import initialize_clients

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

    # ----------------------------------
    # pull images
    # ----------------------------------
    
    # ----- pull team right image
    try:
        tr = data["team_right"]
        client = data["team_right"]["_client"]
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
        tl = data["team_left"]
        client = data["team_left"]["_client"]
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
        rcss = data["rcssserver"]
        client = data["rcssserver"]["_client"]
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
    
    
    # create tasks for streams

    pass
