from aiohttp.web import WebSocketResponse, WSMsgType


async def index(request, ws_pool):
    ws = WebSocketResponse()
    await ws.prepare(request)
    ws_pool.add(ws)

    try:
        async for message in ws:
            if message.type != WSMsgType.text:
                continue
            if message.data != 'close':
                continue
    finally:
        if not ws.closed:
            await ws.close()
        ws_pool.remove(ws)

    return ws
