import asyncio


class WSPool:

    def __init__(self, pool=None):
        if pool is None:
            pool = []
        self._pool = pool

    def add(self, ws):
        self._pool.append(ws)

    def remove(self, ws):
        self._pool.remove(ws)

    async def broadcast(self, data):
        await self._remove_closed_connections_in_pool()
        tasks = [ws.send_json(data) for ws in self._pool]
        await asyncio.gather(
            *tasks,
            return_exceptions=True
        )

    async def _remove_closed_connections_in_pool(self):
        self._pool = [
            ws
            for ws in self._pool
            if not ws.closed
        ]
