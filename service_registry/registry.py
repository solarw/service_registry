from typing import Generator

from .service import Service


class ServiceRegistry(object):
    SERVICE_CLASS = Service

    def __init__(self, notification_queue):
        self._services = {}
        self.notification_queue = notification_queue

    async def notify(self, msg):
        await self.notification_queue.put(msg)

    async def add_service(self, stype, version, data=None):
        service = Service(stype, version, data)
        self._services[service.id] = service
        await self.notify('created')

    async def update_service(self, service_id, data=None):
        assert service_id in self._services, 'Service `{}` not registered!'.format(service_id)
        self._services[service_id].update(data)
        await self.notify('changed')

    async def remove_service(self, service_id: str):
        assert service_id in self._services, 'Service `{}` not registered!'.format(service_id)
        del self._services[service_id]
        await self.notify('removed')

    async def find_services(self, stype: str, version: str=None) -> Generator[Service, None, None]:
        """ generator """
        if not stype:
            for i in self._services.values():
                yield i

        for i in self._services.values():
            if stype is not None and i.type != stype:
                continue
            if version is not None and i.version != version:
                continue
            yield i
