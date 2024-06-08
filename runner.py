import asyncio
import aio_pika

from src.docker import Docker
from src.logger import get_logger
from src.message_handlers.kill_match import kill_match_command_handler
from src.message_handlers.ping import ping_command_handler
from src.message_handlers.run_match import run_match_command_handler
from src.message_handlers.score import score_command_handler
from src.message_handlers.status import status_command_handler
from src.message_hanlder import MessageHandler
from src.rabbitmq import RabbitMQ
from src.routes.status import handle_status
from src.storage import MinioClient
from src.webserver import Webserver




logger = get_logger(__name__)


loop = asyncio.get_event_loop()
tasks = {}
match_task = None


        
async def main(loop):


    # ---------------------- 
    # RabbitMQ
    # ---------------------- 
    rabbit = RabbitMQ(
        loop=loop, 
        server="amqp://test:test@localhost/", 
        queue="my_queue"
    )
    logger.info("rabbitmq consumer started")
    try:
        logger.info("rabbitmq connecting...")
        await rabbit.connect()
        logger.info("rabbitmq connected")
    except Exception as e:
        logger.error("rabbitmq connection failed")
        logger.error(e)
        exit(1)

    
    
    # ----------------------
    # Storage
    # ----------------------
    storage = MinioClient(
        endpoint="localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    try:
        logger.info("storage connecting...")
        storage.connect()
        logger.info("storage connected")
    except Exception as e:
        logger.error("storage connection failed")
        logger.error(e)
        exit(1)
        
        
    # ----------------------
    # Docker
    # ----------------------
    docker = Docker(
        default_registry="localhost:5000",
        username="",
        password=""
    )
    try:
        logger.info("docker connecting...")
        docker.connect()
        logger.info("docker connected")
    except Exception as e:
        logger.error("docker connection failed")
        logger.error(e)
        exit(1)
    
    
    # ----------------------
    # Webserver
    # ----------------------
    server = Webserver(
        host="localhost",
        port=8080
    )
    
    # --- routes
    server.add_get('/status', handle_status)
    try:
        await server.listen()
        logger.info("webserver connected")
    except Exception as e:
        logger.error("webserver connection failed")
        logger.error(e)
        exit(1)
    




    # ----------------------
    
    # --- add message handler
    mh = MessageHandler(
        rabbit=rabbit,
        storage=storage,
        docker=docker,
        server=server
    )
    
    mh.add_command_handler("run_match", run_match_command_handler)
    mh.add_command_handler("kill_match", kill_match_command_handler)
    mh.add_command_handler("score", score_command_handler)
    mh.add_command_handler("status", status_command_handler)
    mh.add_command_handler("ping", ping_command_handler)
    
    
    await rabbit.add_message_handler(mh.message_processor)



if __name__ == "__main__":
    try:
        loop.run_until_complete(main(loop))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
