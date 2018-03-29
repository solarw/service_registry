import asyncio

from aiohttp_json_rpc.client import JsonRpcClientContext


async def rpc_call(url, method_name, *args, **kwargs):
    async with JsonRpcClientContext(url) as jrpc:
        method = getattr(jrpc, method_name)
        method_res = await method(*args, **kwargs)
    return method_res


async def get_one_notification(url, topic):
    ready = asyncio.Future()

    async def handler(msg_data):
        if ready.done():
            return
        ready.set_result(msg_data['params'][0])

    async with JsonRpcClientContext(url) as jrpc:
        await jrpc.subscribe(topic, handler)
        result = await ready

    return result
