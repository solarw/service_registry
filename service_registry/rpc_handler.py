from asyncio.tasks import ensure_future

from aiohttp_json_rpc import JsonRpc


class JsonRpcHandler(object):
    VERSION = 'v1'
    EXPORTED_METHODS = ('add_service', 'remove_service', 'update_service', 'find_services')

    def __init__(self, registry, notification_queue):
        self.rpc = JsonRpc()
        self.rpc.pass_args = True
        self.rpc.add_topics('services')
        self.notification_queue = notification_queue
        self.registry = registry
        self.notifications_handler_task = ensure_future(self.notifications_handler())
        self.register_methods()

    def register_methods(self):
        for method_name in self.EXPORTED_METHODS:
            method = getattr(self, method_name)
            self.rpc.add_methods(('', method))

    def route(self):
        return ('*', '/{}/'.format(self.VERSION), self.rpc)

    async def _get_notification(self):
        return await self.notification_queue.get()

    async def notifications_handler(self):
        while True:
            notification = await self._get_notification()
            await self.rpc.notify('services', notification)

    async def add_service(self, request, type, version, data=None):
        service_id = await self.registry.add_service(type, version, data)
        return service_id

    async def update_service(self, request, service_id, data=None):
        await self.registry.update_service(service_id, data)

    async def remove_service(self, request, service_id):
        await self.registry.remove_service(service_id)

    async def find_services(self, request, type=None, version=None):
        result = [i.__json__() async for i in self.registry.find_services(type, version)]
        return result
