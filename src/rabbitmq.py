import aio_pika

class RabbitMQ:
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