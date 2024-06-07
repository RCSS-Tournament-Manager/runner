import asyncio

from src.storage import MinioClient


async def ping_command_handler(data: dict, storage: MinioClient, **kwargs):
    import os
    await storage.upload_file(
        bucket_name="ping-pong",
        object_name="ping.txt",
        file_path=os.path.join(os.path.dirname(__file__),'..','..', "test.py"),
    )
