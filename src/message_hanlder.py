import aio_pika
import json
import inspect
from src.logger import get_logger
from src.rabbitmq import RabbitMQ

logger = get_logger(__name__)


class MessageHandler:
    def __init__(self, rabbit, storage, docker, server):
        self.rabbit = rabbit
        self.storage = storage
        self.docker = docker
        self.server = server
        self.message_handlers = {}

    def add_command_handler(self, command, handler):
        self.message_handlers[command] = handler

    # reply("something")
    # reply({"key": "value"})
    @staticmethod
    def reply_wrapper(rabbit: RabbitMQ, reply_channel):
        async def reply(message):
            out_message = {}
            
            if type(message) == str:
                out_message["message"] = message
            elif type(message) == dict:
                out_message = message
                
            await rabbit.channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(out_message).encode()),
                routing_key=reply_channel
            )

        return reply

    @staticmethod
    async def empty_reply(*args, **kwargs):
        logger.debug("Empty reply")
        return

    async def message_processor(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = message.body.decode()
            data = json.loads(body)
            command = data.get("command")
            body = data.get("data")
            reply = MessageHandler.empty_reply

            if message.reply_to != None and message.reply_to != "":
                reply = MessageHandler.reply_wrapper(self.rabbit, message.reply_to)

            logger.info(f"Received message: {data}")

            if command in self.message_handlers:
                singletons = {
                    "rabbit": self.rabbit,
                    "storage": self.storage,
                    "docker": self.docker,
                    "server": self.server,
                    "reply": reply,
                }

                function_input = {"data": body, **singletons}

                handler = self.message_handlers[command]

                if inspect.iscoroutinefunction(handler):
                    await handler(**function_input)
                else:
                    handler(**function_input)

            else:
                logger.error(f"Unknown command: {command}")
                logger.debug(f"known commands: {self.message_handlers.keys()}")
                return
