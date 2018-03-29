from behave import given
from behave import then
from behave import when
from behave.api.async_step import async_run_until_complete

from service_registry.utils import get_one_notification
from service_registry.utils import rpc_call


@given('there is an empty ServiceRegistry')
@async_run_until_complete
async def init(context):
    pass


@when('I add a service "{service}" with version "{version}"')
@async_run_until_complete
async def when_add(context, service, version):
    await rpc_call(context.feature.url, 'add_service', service, version)


@when('I update a service')
@async_run_until_complete
async def do_update(context):
    services = await rpc_call(context.feature.url, 'find_services')
    service_id = services[0]['id']
    services = await rpc_call(context.feature.url, 'update_service', service_id, {'some': 'data'})


@when('I remove a service')
@async_run_until_complete
async def do_remove(context):
    services = await rpc_call(context.feature.url, 'find_services')
    context.service_removed = services[0]
    service_id = services[0]['id']
    services = await rpc_call(context.feature.url, 'remove_service', service_id)


@then('the service should be removed')
@async_run_until_complete
async def check_remove(context):
    services = await rpc_call(context.feature.url, 'find_services')
    assert context.service_removed['id'] not in [i['id'] for i in services]


@then('I should be notified with a change "{change}"')
@async_run_until_complete
async def notification(context, change):
    msg = await get_one_notification(context.feature.url, 'services')
    assert change == msg, msg


@when('I search for a service "{service}" with version "{version}"')
@when('I search for a service "{service}" without version')
@async_run_until_complete
async def when_find(context, service, version=None):
    services = await rpc_call(context.feature.url, 'find_services', service, version)
    context.services_found = services


@then('I should find count "{count}" instances of service')
@then('I should find count "{count}" services')
@async_run_until_complete
async def when_found(context, count):
    services_found = len(context.services_found)
    assert services_found == int(count), services_found


@then('the service "{service}" should have the correct type')
@async_run_until_complete
async def type_check(context, service):
    for i in context.services_found:
        assert i['type'] == service, i


@then('the service "{service}" should have the correct version "{version}"')
@async_run_until_complete
async def version_check(context, service, version):
    for i in context.services_found:
        assert i['type'] == service, i
        if version is not None:
            assert i['version'] == version, i
