import base64
import json
import logging
from behave import use_step_matcher, given, when, then
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
import tests.integration.features.steps.common as common

PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDHzEPNqqCOe4I+O834Rlvmm+Fbx3QINyofeBvUWk6zw4YVvzVjlQSxusEdSZwL8WR84YJZyd5iY5MeeM1MjwcA6uVz07CQ+iWALTiD0XXBmr+WguNZ5/zEmznzXJUC8K9YN5lMSGiPPzz1uIaS4pzRjIBy22knzYB8TCAYccSky77h5Ah42BwQaZ8YfjRXHumHaRqqOOrQUDVDF0VTHS31fKbmYiRm01EOumNHLQYgvh6gZfVPa5bNIRt1ZTpiGiBJkDaRIhecz1TWT1J/PasI1F8zcgZff0Sg78NgVB4iJq2aUGf5SBqR/HLvB9IfGtR1xUwG31+sUJJ3mEmop1D6N+WtLHUJM1GfdkRB6/r+u7l+rt/ihdlpYGlbMJxcOtNsGMDPf8dzVlRVm9nVCRTyQd7Da9hYrHDQM5OkrMUOzEGJ3X+V5BdENJu0N07l/ARtq9ctTZBTn/DAojggOd8SPtY0mm1icdQmIZFrdnyShjQ57tZkDYYVJostuJaEEMci9WActyfsWZPvXmzEdJkLTMssr60f27+hJlFiHPEScudIx/8eYpFKaOikSF0eUFm59fwE4PmcLGzPoE+/VyAblHIcxUGDUGKsi/ftFq5xbUOJxqiGkwZqPUXZnchPiRmJLn2LT+zdsvVF57tpCIwuyNseI6NoGqgq/tR2O8an2Q== vscode@19fad2f77a4d"

use_step_matcher("re")

from pydantic import BaseModel

class GenerateTokenRequest(BaseModel):
    role_name: str

    def to_api(self) -> apiv1.GenerateTokenRequest:
        return apiv1.GenerateTokenRequest(role_name="role_name")

@when(u'Клиент вызывает GenerateToken\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    spec = GenerateTokenRequest(**json.loads(context.text))

    await do_rpc(
        context,
        stub.GenerateToken,
        spec.to_api()
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

class Token(BaseModel):
    role_name: str

@then(u'токен содержит поле role_name, равное значению role_name, переданому в Запросе')
def step_impl(context: behave_runner.Context):
    spec = Token(**json.loads(context.text))
    assert context.decoded_token["role"] == spec.role_name

@then(u'Сервис отправляет Ответ со статусом INVALID_ARGUMENT')
def step_impl(context: behave_runner.Context):
    assert context.status == grpc.StatusCode.INVALID_ARGUMENT
