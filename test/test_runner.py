import sys
import asyncio
import aio_pika

match_kill = False
async def worker(message: aio_pika.IncomingMessage, channel):
    async with message.process():
        global match_kill
        cmd = message.body.decode()
        reply_channel = message.reply_to
        
        if cmd == "run_match":
            print("Match started, running for 30 seconds...")
            # send reply every 1 second to chnnael for 30 second
            for i in range(30):
                
                if match_kill == True :
                    await channel.default_exchange.publish(
                        aio_pika.Message(
                            body="bemola kill shodam".encode()
                        ),
                        routing_key=reply_channel
                    )
                    break
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=f"Match running for {i+1} seconds".encode()
                    ),
                    routing_key=reply_channel
                )
                await asyncio.sleep(1)

            print("Match finished.")
        
        if cmd == "kill_match":
            print("Received kill command, stopping in 5 seconds...")
            await asyncio.sleep(5)  # Simulate stopping match
            match_kill = True
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body="Match killed".encode()
                ),
                routing_key=reply_channel
            )
            print("Match killed.")

async def run():
    connection = await aio_pika.connect_robust("amqp://test:test@localhost/")
    runner_name = sys.argv[1]
    
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(runner_name)
        print("Runner is listening for commands...")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                loop = asyncio.get_event_loop()
                loop.create_task(worker(message,channel))
