import asyncio
import aio_pika

RABBITMQ_URL = "amqp://guest:guest@localhost/"
REQUEST_QUEUE_NAME = "request_queue"
RESPONSE_QUEUE_NAME = "response_queue"


async def send_message(loop):
    connection = await aio_pika.connect_robust(RABBITMQ_URL, loop=loop)

    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(REQUEST_QUEUE_NAME, durable=True)

        message_body = "Hello, this is a request message."
        correlation_id = "1234"

        # Publish a message with a reply_to property
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body.encode(),
                reply_to=RESPONSE_QUEUE_NAME,
                correlation_id=correlation_id,
            ),
            routing_key=REQUEST_QUEUE_NAME,
        )
        print(f"Sent: {message_body}")

        # Set up a consumer on the response queue
        await receive_response(connection, correlation_id)


async def receive_response(connection, correlation_id):
    async with connection:
        channel = await connection.channel()
        response_queue = await channel.declare_queue(RESPONSE_QUEUE_NAME, durable=True)

        async with response_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    if message.correlation_id == correlation_id:
                        response_body = message.body.decode()
                        print(f"Received response: {response_body}")
                        break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message(loop))
