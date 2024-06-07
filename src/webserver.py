from aiohttp import web
from src.logger import get_logger
logger = get_logger(__name__)

class Webserver:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.runner = None

    async def listen(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()
        logger.info(f'web serving on http://{self.host}:{self.port}')

    async def stop(self):
        if self.runner:
            await self.runner.cleanup()

    def add_get(self, url, function):
        self.app.router.add_get(url, function)

    def add_post(self, url, function):
        self.app.router.add_post(url, function)

    def add_patch(self, url, function):
        self.app.router.add_patch(url, function)

    def add_delete(self, url, function):
        self.app.router.add_delete(url, function)

    def add_put(self, url, function):
        self.app.router.add_put(url, function)
