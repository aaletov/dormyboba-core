import json
import datetime
import behave.runner as behave_runner
from behave.api.async_step import async_run_until_complete
from behave import given, when, then
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from google.protobuf.empty_pb2 import Empty
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
import dormyboba_core.model as model
from tests.integration.features.steps.wrapper import do_rpc

# Import common steps so decorator will be invoked
import tests.integration.features.steps.common as common

def parse_queue(context: behave_runner. Context) -> dict:
    return json.loads(context.text)

@when(u'Клиент вызывает CreateQueue() rpc с запросом')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    when_queue = parse_queue(context)
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    when_open = datetime.datetime.strptime(when_queue["open"], '%Y-%m-%d %H:%M:%S.%f')
    await do_rpc(
        context,
        stub.CreateQueue,
        apiv1.CreateQueueRequest(
            apiv1.Queue(
                title=when_queue["title"],
                open=when_queue["open"],
            ),
        ),
    )

@then(u'Ответ содержит информацию о простой очереди')
def step_impl(context: behave_runner.Context):
    res: apiv1.CreateQueueResponse = context.response
    then_queue = parse_queue(context)
    then_open = datetime.datetime.strptime(then_queue["open"], '%Y-%m-%d %H:%M:%S.%f')
    assert res.queue.HasField("queue_id")
    assert then_queue["title"] == res.queue.title
    assert then_open == res.queue.open

@given(u'в базе есть пустая очередь с queue_id = 3')
def step_impl(context: behave_runner.Context):
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        model_queue = model.Queue(
            queue_id=3,
            title="Title",
            open=datetime.datetime.now(),
            is_event_generated=True,
        )
        session.add(model_queue)


@given(u'в базе есть пользователь с user_id = 4')
def step_impl(context: behave_runner.Context):
    common.add_standard_roles(context)
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        role = session.scalar(
            select(model.DormybobaRole)
            .limit(1)
        )
        user = model.DormybobaUser(
            user_id=4,
            role=role,
            registration_complete=False,
        )
        session.add(user)

def parse_add_person_to_queue_request(context: behave_runner. Context) -> dict:
    return json.loads(context.text)

@when(u'Клиент вызывает AddPersonToQueue() rpc с запросом')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    req = parse_add_person_to_queue_request(context)
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(
        context,
        stub.AddPersonToQueue,
        apiv1.AddPersonToQueueRequest(
            queue_id=req["queue_id"],
            user_id=req["user_id"],
        ),
    )

@then(u'Ответ содержит информацию о том, что добавленный пользователь является активным пользователем в очереди')
def step_impl(context: behave_runner.Context):
    res: apiv1.AddPersonToQueueResponse = context.response
    assert res.is_active

@given(u'в базе есть непустая очередь с queue_id = 3')
def step_impl(context: behave_runner.Context):
    common.add_standard_roles(context)
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        model_queue = model.Queue(
            queue_id=3,
            title="Title",
            open=datetime.datetime.now(),
            is_event_generated=True,
        )
        session.add(model_queue)
        model_role = session.scalar(
            select(model.DormybobaRole)
            .limit(1)
        )
        model_user = model.DormybobaUser(
            user_id=4,
            role=model_role,
            registration_complete=False,
        )
        session.add(model_user)
        model_qtu = model.QueueToUser(
            queue_id=model_queue.queue_id,
            user_id=model_user.user_id,
            joined=datetime.datetime.now(),
        )
        session.add(model_qtu)

@then(u'Ответ содержит информацию о том, что добавленный пользователь не является активным пользователем в очереди')
def step_impl(context: behave_runner.Context):
    res: apiv1.AddPersonToQueueResponse = context.response
    assert not(res.is_active)

@given(u'в базе есть пользователь с user_id = 4, находящийся в очереди с queue_id = 3')
def step_impl(context: behave_runner.Context):
    common.add_standard_roles(context)
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        model_queue = model.Queue(
            queue_id=3,
            title="Title",
            open=datetime.datetime.now(),
            is_event_generated=True,
        )
        session.add(model_queue)
        model_role = session.scalar(
            select(model.DormybobaRole)
            .limit(1)
        )
        model_user = model.DormybobaUser(
            user_id=4,
            role=model_role,
            registration_complete=False,
        )
        session.add(model_user)
        model_qtu = model.QueueToUser(
            queue_id=model_queue.queue_id,
            user_id=model_user.user_id,
            joined=datetime.datetime.now(),
        )
        session.add(model_qtu)

def parse_remove_person_from_queue_request(context: behave_runner. Context) -> dict:
    return json.loads(context.text)

@when(u'Клиент вызывает RemovePersonFromQueue() rpc с запросом')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    req = parse_remove_person_from_queue_request(context)
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(
        context,
        stub.RemovePersonFromQueue,
        apiv1.RemovePersonFromQueueRequest(
            queue_id=req["queue_id"],
            user_id=req["user_id"],
        ),
    )

@given(u'активным пользователем в очереди с queue_id = 3 является пользователь с user_id = 4')
def step_impl(context: behave_runner.Context):
    common.add_standard_roles(context)
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        model_role = session.scalar(
            select(model.DormybobaRole)
            .limit(1)
        )
        model_user = model.DormybobaUser(
            user_id=4,
            role=model_role,
            registration_complete=False,
        )
        session.add(model_user)
        model_qtu = model.QueueToUser(
            queue_id=3,
            user_id=model_user.user_id,
            joined=datetime.datetime.now(),
        )
        session.add(model_qtu)

def parse_person_complete_queue_request(context: behave_runner. Context) -> dict:
    return json.loads(context.text)

@when(u'Клиент вызывает PersonCompleteQueueRequest() rpc с запросом')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    req: apiv1.PersonCompleteQueueRequest = parse_person_complete_queue_request(context)
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(
        context,
        stub.PersonCompleteQueue,
        apiv1.PersonCompleteQueueRequest(
            queue_id=req["queue_id"],
            user_id=req["user_id"],
        ),
    )

def parse_person_complete_queue_response(context: behave_runner. Context) -> dict:
    return json.loads(context.text)

@then(u'Ответ содержит информацию о том, что очередь теперь пуста')
def step_impl(context: behave_runner.Context):
    then_req = parse_person_complete_queue_response(context)
    res: apiv1.PersonCompleteQueueResponse = context.response
    assert res.is_queue_empty == then_req["is_queue_empty"]
    assert not(res.HasField("active_user_id"))
