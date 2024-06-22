import aio_pika
from aiostomp import AioStomp

from src.logger import get_logger


logger = get_logger(__name__)

# --- AMQP Protocol --- (OLD)
class RabbitMQAMQP:
    def __init__(self, loop, server, queue):
        self.loop = loop
        self.server = server
        self.queue = queue
        self.connection = None
        self.channel = None
        self.queue_instance = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.server, loop=self.loop)
        self.channel = await self.connection.channel()
        self.queue_instance = await self.channel.declare_queue(self.queue)

    async def close(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
    
    async def add_message_handler(self, handler):
        self.loop.create_task(self.queue_instance.consume(handler))
        
        
        

class StompClient:
    def __init__(self, loop, server, port, queue, username, password):
        self.loop = loop
        self.server = server
        self.port = port
        self.queue = queue
        self.username = username
        self.password = password
        self.client = None

    async def connect(self):
        self.client = AioStomp(self.server, self.port, error_handler=self.report_error)
        await self.client.connect(self.username, self.password)
    
    async def close(self):
        if self.client:
            await self.client.disconnect()
    
    async def add_message_handler(self, handler):
        self.client.subscribe(self.queue, handler=handler)
    
    
    async def report_error(self, error):
        logger.error(f"Error: {error}")
        
    async def send_message(self, message, queue=None, headers=None):
        target_queue = queue if queue else self.queue
        self.client.send(target_queue, body=message, headers=headers if headers else {"x-expires": 10})
        
RabbitMQ = StompClient