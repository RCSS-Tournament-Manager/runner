import asyncio
import aio_pika
import json
import os
from src.storage import MinioClient
from src.logger import get_logger

import random
logger = get_logger(__name__)


def data():
   return  {
    "command": "run_match",
    "data": {
        "match_id": "1234",
        
        "team_right": {
            "_type": "docker",
            "image_name": "cyrus2d",
            "tag": "latest",
            "team_name": "cyrusA",
            "config": {
                "core_start": 0,
                "core_end": 11,
            }
        },
        
        "team_left": {
            "_type": "docker",
            "image_name": "cyrus2d",
            "tag": "latest",
            "team_name": "cyrusB",
            "config": {
                "core_start": 0,
                "core_end": 11,
            }
        },
        
        
        "rcssserver": {
            "_type": "docker",
            "image_name": "rcssserver",
            "tag": "latest",
            "config": {
                "core_start": 0,
                "core_end": 11,
            },
            "rcssserver_config": {
            },
            
        },
        
        
        
        "log": {
            "level": "info",
            
            "s3":{
                "config": {
                    "type": "minio",
                    "endpoint": "http://minio:9000",
                    "access_key": "access_key",
                    "secret_key": "secret_key",
                    "bucket": "bucket",
                },
                "right_team_log" : "true",
                "left_team_log" : "true",
                "server_log" : "true",
                "rcg" : "true",
                "rcl" : "true",
            },
            
            "stream": {
                "config": {
                    "type": "rabbitmq",
                    "host": "rabbitmq",
                    "port": 5672,
                    "username": "username",
                    "password": "password",
                    "exchange": "exchange",
                    "queue": "queue",                    
                },
                "right_team_log" : "true" or {
                    "queue": "queue",    
                },
                "left_team_log" : {
                    "type": "rabbitmq",
                    "host": "rabbitmq",
                    "port": 5672,
                    "queue": "queue",
                },
                "server_log" : "true",
                "rcg" : "true",
                "rcl" : "true",
                "score" : "true",
            }
        }
        
        
        
    }
}

def log(msg):
    print (f' [+] {msg}')



async def send_run_message(channel,send_queue):
    # create a channel for getting the reply
    reply_queue = await channel.declare_queue(exclusive=True)
    print(f"The name of the declared queue is: {reply_queue.name}")
    
    msg = data()
    # Sending run_match command
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(msg).encode(),
            reply_to=reply_queue.name
        ),
        routing_key=send_queue
    )
    
    log(f"Sent 'run' command. on {send_queue}")

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
        loop.create_task(send_run_message(channel,"runner_queue"))


        # wait for all tasks to be done
        await asyncio.gather(*asyncio.all_tasks())