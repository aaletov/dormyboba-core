import json
import behave.runner as behave_runner
from behave import given, when, then
from behave.api.async_step import async_run_until_complete
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
import dormyboba_core.model as model
from tests.integration.features.steps.wrapper import do_rpc

# Import common steps so decorator will be invoked
import tests.integration.features.steps.common as common

def parse_user(context: behave_runner. Context) -> dict:
    return json.loads(context.text)

@given(u'в базе содержится информация о пользователе')
def step_impl(context: behave_runner.Context):
    common.add_standard_roles(context)
    given_user = parse_user(context)
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        role = session.scalar(
            select(model.DormybobaRole)
            .where(model.DormybobaRole.role_name == given_user["role_name"])
        )
        assert role != None
        user = model.DormybobaUser(
            user_id=given_user["user_id"],
            role=role,
            registration_complete=False,
        )
        session.add(user)

@when(u'Клиент вызывает UpdateUser() rpc с запросом')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    when_user = parse_user(context)
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(context, stub.UpdateUser, apiv1.UpdateUserRequest(
        user=apiv1.DormybobaUser(
            user_id=when_user["user_id"],
            role=apiv1.DormybobaRole(
                role_name=when_user["role_name"],
            ),
        ),
    ))

@then(u'Ответ содержит информацию о пользователе')
def step_impl(context: behave_runner.Context):
    response: apiv1.UpdateUserResponse = context.response
    then_user = parse_user(context)
    assert response.user.user_id == then_user["user_id"]
    assert response.user.role.role_name == then_user["role_name"]

@given(u'в базе не содержится пользователей')
def step_impl(context: behave_runner.Context):
    pass

@when(u'Клиент вызывает GetUserById() rpc с user_id = 3')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(
        context,
        stub.GetUserById,
        apiv1.GetUserByIdRequest(
            user_id=3,
        ),
    )
