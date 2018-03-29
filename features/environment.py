import asyncio

from aiohttp.web import Application

from service_registry import NotificationQueue
from service_registry import ServiceRegistry
from service_registry.rpc_handler import JsonRpcHandler


HOST = '127.0.0.1'
PORT = '48888'
VERSION = 'v1'


def before_feature(context, feature):
    loop = asyncio.get_event_loop()

    notification_queue = NotificationQueue()
    registry = ServiceRegistry(notification_queue)
    json_rpc_handler = JsonRpcHandler(registry, notification_queue)

    feature.url = 'ws://{}:{}/{}/'.format(HOST, PORT, VERSION)
    app = Application(loop=loop)
    app.router.add_route(*json_rpc_handler.route())

    handler = app.make_handler()
    feature.loop = loop
    feature.server = loop.run_until_complete(loop.create_server(handler, HOST, PORT))


def after_feature(context, feature):
    feature.server.close()
    feature.loop.run_until_complete(feature.server.wait_closed())
