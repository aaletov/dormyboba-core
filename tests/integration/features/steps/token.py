import base64
import logging
from behave import given, when, then
import behave.runner as behave_runner
from behave.api.async_step import async_run_until_complete
import grpc
import jwt
import google.protobuf.json_format as gpjson
from sqlalchemy.orm import Session
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
from dormyboba_core.entity import Token
import dormyboba_core.model as model
from tests.integration.features.steps.wrapper import do_rpc

# Import common steps so decorator will be invoked
import tests.integration.features.steps.wrapper

PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDHzEPNqqCOe4I+O834Rlvmm+Fbx3QINyofeBvUWk6zw4YVvzVjlQSxusEdSZwL8WR84YJZyd5iY5MeeM1MjwcA6uVz07CQ+iWALTiD0XXBmr+WguNZ5/zEmznzXJUC8K9YN5lMSGiPPzz1uIaS4pzRjIBy22knzYB8TCAYccSky77h5Ah42BwQaZ8YfjRXHumHaRqqOOrQUDVDF0VTHS31fKbmYiRm01EOumNHLQYgvh6gZfVPa5bNIRt1ZTpiGiBJkDaRIhecz1TWT1J/PasI1F8zcgZff0Sg78NgVB4iJq2aUGf5SBqR/HLvB9IfGtR1xUwG31+sUJJ3mEmop1D6N+WtLHUJM1GfdkRB6/r+u7l+rt/ihdlpYGlbMJxcOtNsGMDPf8dzVlRVm9nVCRTyQd7Da9hYrHDQM5OkrMUOzEGJ3X+V5BdENJu0N07l/ARtq9ctTZBTn/DAojggOd8SPtY0mm1icdQmIZFrdnyShjQ57tZkDYYVJostuJaEEMci9WActyfsWZPvXmzEdJkLTMssr60f27+hJlFiHPEScudIx/8eYpFKaOikSF0eUFm59fwE4PmcLGzPoE+/VyAblHIcxUGDUGKsi/ftFq5xbUOJxqiGkwZqPUXZnchPiRmJLn2LT+zdsvVF57tpCIwuyNseI6NoGqgq/tR2O8an2Q== vscode@19fad2f77a4d"

@when(u'Клиент вызывает GenerateToken() rpc с корректным значением роли')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    with Session(context.engine) as session, session.begin():
        roles = [
            model.DormybobaRole(role_name="student"),
            model.DormybobaRole(role_name="council_member"),
            model.DormybobaRole(role_name="admin"),
        ]
        session.add_all(roles)
    stub: apiv1grpc.DormybobaCoreStub = context.stub

    await do_rpc(
        context,
        stub.GenerateToken,
        apiv1.GenerateTokenRequest(
            role_name="student",
        ),
    )

@then(u'Ответ содержит поле token, содержащее корректный base64 закодированный JWT-токен')
def step_impl(context: behave_runner.Context):
    response: apiv1.GenerateTokenResponse = context.response
    once_encoded = base64.b64decode(response.token.encode("utf-8"))
    decoded = jwt.decode(once_encoded, key=PUBLIC_KEY, algorithms=["RS256"])
    context.decoded_token = decoded

@then(u'токен должен быть подписан приватным ключом приложения')
def step_impl(context: behave_runner.Context):
    pass

@then(u'токен содержит поле role_name, равное значению role_name, переданому в Запросе')
def step_impl(context: behave_runner.Context):
    assert context.decoded_token["role"] == "student"

@when(u'Клиент вызывает GenerateToken() rpc с некорректным значением роли')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(
        context,
        stub.GenerateToken,
        apiv1.GenerateTokenRequest(
            role_name="bebra",
        ),
    )

@then(u'Сервис отправляет Ответ со статусом INVALID_ARGUMENT')
def step_impl(context: behave_runner.Context):
    assert context.status == grpc.StatusCode.INVALID_ARGUMENT
