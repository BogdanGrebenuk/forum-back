import asyncio

import aiohttp


URL = f'http://localhost:8000/ws'


async def exit_if_required():
    if input() == 'exit':
        print('Exiting. Cause: client')
        raise SystemExit(0)


async def main():
    session = aiohttp.ClientSession(headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTg5ZGMwMmUtMjg4Ny00MmU4LWI2NzItN2Y1OWQ1ZWY5Y2NiIiwic2FsdCI6IjdiNGE4OWU2LTJmY2QtNGVkNC1hMWVmLTQ3MGM1YjM3OTk4NyJ9.qXKTJL-0EIIe7erzXuYcGiVD5LjE2OIQvL2Fbgqaf7I'})
    async with session.ws_connect(URL) as ws:
        async for msg in ws:
            print('Message received from server:', msg)
            if msg.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                print('Exiting. Cause: server')
                break
            # await exit_if_required()


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
