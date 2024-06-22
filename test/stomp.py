import sys
import logging
import asyncio

from aiostomp import AioStomp

logging.basicConfig(
    format="%(asctime)s - %(filename)s:%(lineno)d - "
    "%(levelname)s - %(message)s",
    level='INFO')

# mute aiostomp.py
logging.getLogger('aiostomp').setLevel('INFO')


async def run():
    client = AioStomp('localhost', 61613, error_handler=report_error)
    client.subscribe('/queue/test', handler=on_message)

    await client.connect('admin','admin')

    client.send('/queue/test', body=u'Thanks', headers={})
    


async def on_message(frame, message):
    print('on_message:', message)
    return True


async def report_error(error):
    print('report_error:', error)
