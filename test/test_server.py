import asyncio
import aio_pika


def log(msg):
    print (f' [+] {msg}')


async def send_kill_message(channel,send_queue):
    # create a channel for getting the reply
    reply_queue = await channel.declare_queue(exclusive=True)
    print(f"The name of the declared queue is: {reply_queue.name}")
    
    # Sending run_match command
    await channel.default_exchange.publish(
        aio_pika.Message(
            body="kill_match".encode(),
            reply_to=reply_queue.name
        ),
        routing_key=send_queue
    )
    
    log(f"Sent 'kill_match' command. on {send_queue}")

    # print the reply from the queue
    async with reply_queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print(f" [x] Received reply from {send_queue}:", message.body.decode())
                # it means it is finished
                if "finished" in message.body.decode():
                    break


async def send_run_message(channel,send_queue):
    # create a channel for getting the reply
    reply_queue = await channel.declare_queue(exclusive=True)
    print(f"The name of the declared queue is: {reply_queue.name}")
    
    # Sending run_match command
    await channel.default_exchange.publish(
        aio_pika.Message(
            body="run_match".encode(),
            reply_to=reply_queue.name
        ),
        routing_key=send_queue
    )
    
    log(f"Sent 'run_match' command. on {send_queue}")

    # print the reply from the queue
    async with reply_queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print(f" [x] Received reply from {send_queue}:", message.body.decode())
                # it means it is finished
                if "killed" in message.body.decode():
                    break

async def run():
    connection = await aio_pika.connect_robust("amqp://test:test@localhost/")
    loop  = asyncio.get_event_loop()
    async with connection:
        channel = await connection.channel()
        loop.create_task(send_run_message(channel,"runner1"))
        # wait for 10 second
        await asyncio.sleep(10)
        loop.create_task(send_kill_message(channel,"runner1"))
        # wait for 2 second
        await asyncio.sleep(2)
        loop.create_task(send_run_message(channel,"runner2"))
        # wait for 10 second
        await asyncio.sleep(10)
        loop.create_task(send_kill_message(channel,"runner2"))
        
        # wait for all tasks to be done
        await asyncio.gather(*asyncio.all_tasks())
        
