#!/usr/bin/env python3.6
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)
from aiohttp.web import Application
import asyncio
from service_registry import ServiceRegistry
from service_registry import NotificationQueue
from service_registry import JsonRpcHandler


argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--host", help="host to listen. default 0.0.0.0", type=str, default='0.0.0.0')
argument_parser.add_argument("--port", help="port to listen. default 8888", type=int, default=8888)

args = argument_parser.parse_args()


loop = asyncio.get_event_loop()
notification_queue = NotificationQueue()
registry = ServiceRegistry(notification_queue)
json_rpc_handler = JsonRpcHandler(registry, notification_queue)


app = Application(loop=loop)
app.router.add_route(*json_rpc_handler.route())

handler = app.make_handler()
server = loop.run_until_complete(loop.create_server(handler, args.host, args.port))
logging.info('Service started on {}:{}'.format(args.host, args.port))
loop.run_forever()
