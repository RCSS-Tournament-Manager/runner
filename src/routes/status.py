from aiohttp import web

async def handle_status(request):
    data = {
        "running": True,
        "tasks": [],
    }
    return web.json_response(data)
