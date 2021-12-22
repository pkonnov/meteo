import asyncio

from server import get_http_server


async def run():
    server = get_http_server()
    await asyncio.create_task(server.serve())


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([run()], return_when=asyncio.FIRST_EXCEPTION))
