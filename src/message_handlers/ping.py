import asyncio

from src.decorators import required_fields
from src.docker import Docker
from src.logger import get_logger
from src.storage import MinioClient

logger = get_logger(__name__)

@required_fields(fields=[
    "file.bucket",
    
    "build_id",
        
    "image_name",
    "image_tag",
    
    "file.type",
    "file.file_id",
])
async def ping_command_handler(
    data: dict, 
    docker: Docker,
    storage: MinioClient,
    reply, 
    **kwargs
):
    await reply("Pong")
