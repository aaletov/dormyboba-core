import logging
import json
import behave.runner as behave_runner
from behave import use_step_matcher, given, when, then
from behave.api.async_step import async_run_until_complete
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
import dormyboba_core.model as model
import dormyboba_core.entity as entity
from tests.integration.features.steps.wrapper import do_rpc

# Import common steps so decorator will be invoked
import tests.integration.features.steps.common as common

use_step_matcher("re")

from pydantic import BaseModel

class UpdateUserRequest(BaseModel):
    user: common.DormybobaUser

    def to_api(self) -> apiv1.UpdateUserRequest:
        return apiv1.UpdateUserRequest(
            user=self.user.to_api(),
        )

@when(u'Клиент вызывает UpdateUser\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    spec = UpdateUserRequest(
        user=common.DormybobaUser(**json.loads(context.text)),
    )

    await do_rpc(context, stub.UpdateUser, spec.to_api())

@then(u'Ответ содержит информацию о пользователе')
def step_impl(context: behave_runner.Context):
    response: apiv1.UpdateUserResponse = context.response
    spec = common.DormybobaUser(**json.loads(context.text))
    assert response.user.user_id == spec.user_id
    assert response.user.role.role_name == spec.role.role_name

@given(u'в базе не содержится пользователей')
def step_impl(context: behave_runner.Context):
    pass

class GetUserByIdRequest(BaseModel):
    user_id: int

    def to_api(self) -> apiv1.GetUserByIdRequest:
        return apiv1.GetUserByIdRequest(user_id=self.user_id)

@when(u'Клиент вызывает GetUserById\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    spec = GetUserByIdRequest(**json.loads(context.text))

    await do_rpc(context, stub.GetUserById, spec.to_api())
