import asyncio
from asyncio.queues import Queue


class NotificationQueue(object):
    def __init__(self, maxsize=None):
        self._queue = Queue(maxsize or 0)

    async def put(self, item):
        await self._queue.put(item)

    async def get(self):
        return await self._queue.get()

    async def purge(self):
        await asyncio.sleep(0)  # to keep queue waiters processed if item was added in this cycle
        self._queue._queue.clear()
