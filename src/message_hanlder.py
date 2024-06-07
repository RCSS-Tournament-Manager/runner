import aio_pika
import json
import inspect
from src.logger import get_logger
logger=get_logger(__name__)

class MessageHandler:
    def __init__(self, rabbit, storage, docker, server):
        self.rabbit = rabbit
        self.storage = storage
        self.docker = docker
        self.server = server
        self.message_handlers = {}

    def add_command_handler(self, command, handler):
        self.message_handlers[command] = handler

    async def message_processor(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = message.body.decode()
            data = json.loads(body)
            command = data.get("command")
            
            logger.info(f"Received message: {data}")
            
            
            if command in self.message_handlers:
                handler = self.message_handlers[command]

                if inspect.iscoroutinefunction(handler):
                    await handler(
                        data=data,
                        rabbit=self.rabbit,
                        storage=self.storage,
                        docker=self.docker,
                        server=self.server,
                    )
                else:
                    handler(
                        data=data,
                        rabbit=self.rabbit,
                        storage=self.storage,
                        docker=self.docker,
                        server=self.server,
                    )

            else:
                logger.error(f"Unknown command: {command}")
                logger.debug(f"known commands: {self.message_handlers.keys()}")
                return
    