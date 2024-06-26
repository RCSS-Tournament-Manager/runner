import json
import inspect
from aiostomp import AioStomp
from src.logger import get_logger
from src.rabbitmq import RabbitMQ

logger = get_logger(__name__)

class MessageHandler:
    singletons = {}
    
    def __init__(self, **singletons):
        self.singletons = singletons
        self.message_handlers = {}

    def add_command_handler(self, command, handler):
        """Try to connect messages to its function

        Args:
            command (str): command type (like: build)
            handler: function that should run for this command 
        """
        self.message_handlers[command] = handler

    @staticmethod
    def reply_wrapper(rabbit: RabbitMQ, reply_channel):
        async def reply(message):
            """Replying the input command

            Args:
                message (str): replying text
            """
            out_message = {}

            if isinstance(message, str):
                out_message["message"] = message
            elif isinstance(message, dict):
                out_message = message

            await rabbit.send_message(json.dumps(out_message), queue=reply_channel)

        return reply

    @staticmethod
    async def empty_reply(*args, **kwargs):
        logger.info("Empty reply")
        return

    async def message_processor(self, frame, message):
        """Take the json message from sender and process its data 

        Args:
            message (str): message from provider
        """
        data = json.loads(message)
        command = data.get("command")
        body = data.get("data")
        reply = MessageHandler.empty_reply

        if 'reply-to' in frame.headers:
            reply = MessageHandler.reply_wrapper(
                self.singletons.get('rabbit'), 
                frame.headers['reply-to']
            )

        print(frame.headers)
        logger.info(f"Received message: {data}")

        if command in self.message_handlers:
            function_input = {
                "data": body, 
                "reply": reply, 
                **self.singletons
            }

            handler = self.message_handlers[command]

            if inspect.iscoroutinefunction(handler):
                await handler(**function_input)
            else:
                handler(**function_input)
        else:
            logger.error(f"Unknown command: {command}")
            logger.debug(f"Known commands: {self.message_handlers.keys()}")
            return
