from typing import Optional
import json
import datetime
import behave.runner as behave_runner
from behave.api.async_step import async_run_until_complete
from behave import use_step_matcher, given, when, then
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from google.protobuf.empty_pb2 import Empty
from google.protobuf.timestamp_pb2 import Timestamp
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
import dormyboba_core.model as model
from tests.integration.features.steps.wrapper import do_rpc

# Import common steps so decorator will be invoked
import tests.integration.features.steps.common as common

from pydantic import BaseModel

class Queue(BaseModel):
    queue_id: int
    title: str
    open: str
    event_generated: bool
    active_user_id: Optional[int] = None

    def to_api(self) -> apiv1.Queue:
        dt_open = datetime.datetime.strptime(self.open, '%Y-%m-%d %H:%M:%S.%f')
        return apiv1.Queue(
            queue_id=self.queue_id,
            title=self.title,
            open=common.dt_to_timestamp(dt_open)
        )

    def to_model(self) -> model.Queue:
        dt_open = datetime.datetime.strptime(self.open, '%Y-%m-%d %H:%M:%S.%f')
        return model.Queue(
            queue_id=self.queue_id,
            title=self.title,
            open=dt_open,
            event_generated=self.event_generated,
            active_user_id=self.active_user_id,
        )

use_step_matcher("re")

@when(u'Клиент вызывает CreateQueue\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    spec = Queue(**json.loads(context.text))
    await do_rpc(
        context,
        stub.CreateQueue,
        apiv1.CreateQueueRequest(
            queue=spec.to_api(),
        ),
    )

@given(u'в базе есть очередь(?P<anything>.*)')
def step_impl(context: behave_runner.Context, anything: str):
    spec = Queue(**json.loads(context.text))
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        session.add(spec.to_model())

@then(u'Ответ содержит информацию об очереди')
def step_impl(context: behave_runner.Context):
    api_spec = Queue(**json.loads(context.text)).to_api()
    res: apiv1.CreateQueueResponse = context.response
    assert res.queue.HasField("queue_id")
    assert api_spec.title == res.queue.title
    assert api_spec.open == res.queue.open.ToDatetime()

class AddPersonToQueueRequest(BaseModel):
    queue_id: int
    user_id: int

    def to_api(self) -> apiv1.AddPersonToQueueRequest:
        return apiv1.AddPersonToQueueRequest(
            queue_id=self.queue_id,
            user_id=self.user_id,
        )

@when(u'Клиент вызывает AddPersonToQueue\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    spec = AddPersonToQueueRequest(**json.loads(context.text))
    await do_rpc(
        context,
        stub.AddPersonToQueue,
        spec.to_api(),
    )

@then(u'Ответ содержит информацию о том, что добавленный пользователь является активным пользователем в очереди')
def step_impl(context: behave_runner.Context):
    res: apiv1.AddPersonToQueueResponse = context.response
    assert res.is_active

@then(u'Ответ содержит информацию о том, что добавленный пользователь не является активным пользователем в очереди')
def step_impl(context: behave_runner.Context):
    res: apiv1.AddPersonToQueueResponse = context.response
    assert not(res.is_active)

class RemovePersonFromQueueRequest(BaseModel):
    queue_id: int
    user_id: int

    def to_api(self) -> apiv1.RemovePersonFromQueueRequest:
        return apiv1.RemovePersonFromQueueRequest(
            queue_id=self.queue_id,
            user_id=self.user_id,
        )

@when(u'Клиент вызывает RemovePersonFromQueue\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    spec = RemovePersonFromQueueRequest(**json.loads(context.text))
    await do_rpc(
        context,
        stub.RemovePersonFromQueue,
        spec.to_api()
    )

class PersonCompleteQueueRequest(BaseModel):
    queue_id: int
    user_id: int

    def to_api(self) -> apiv1.PersonCompleteQueueRequest:
        return apiv1.PersonCompleteQueueRequest(
            queue_id=self.queue_id,
            user_id=self.user_id,
        )

@when(u'Клиент вызывает PersonCompleteQueue\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    spec = PersonCompleteQueueRequest(**json.loads(context.text))
    await do_rpc(
        context,
        stub.PersonCompleteQueue,
        spec.to_api(),
    )

class PersonCompleteQueueResponse(BaseModel):
    is_queue_empty: bool
    active_user_id: Optional[int] = None

    def to_api(self) -> apiv1.PersonCompleteQueueResponse:
        return apiv1.PersonCompleteQueueResponse(
            is_queue_empty=self.is_queue_empty,
            active_user_id=self.active_user_id,
        )


@then(u'Ответ содержит информацию о том, что очередь теперь пуста')
def step_impl(context: behave_runner.Context):
    res: apiv1.PersonCompleteQueueResponse = context.response
    spec = PersonCompleteQueueResponse(**json.loads(context.text))
    assert spec.is_queue_empty == res.is_queue_empty
