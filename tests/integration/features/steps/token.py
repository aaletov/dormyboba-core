import os
import subprocess
import pathlib
import importlib
from behave import given, when, then
import grpc
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc

TEST_CORE_ADDR = "dormyboba_core:50051"

def before_all(context):
    channel = grpc.aio.insecure_channel(TEST_CORE_ADDR)
    stub = apiv1grpc.DormybobaCoreStub(channel)
    context.stub = stub

@when(u'Клиент вызывает GenerateToken() rpc с корректным значением роли')
def step_impl(context):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    try:
        context.response = stub.GenerateToken(
            apiv1.GenerateTokenRequest(
                role_name="student",
            ),
        )
        context.status = grpc.StatusCode.OK
    except grpc.RpcError as exc:
        context.status = exc.code()

@then(u'Сервис отправляет Ответ со статусом OK')
def step_impl(context):
    assert context.status == grpc.StatusCode.OK

@then(u'Ответ содержит поле token, содержащее корректный base64 закодированный JWT-токен')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Ответ содержит поле token, содержащее корректный base64 закодированный JWT-токен')


@then(u'токен должен быть подписан приватным ключом приложения')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then токен должен быть подписан приватным ключом приложения')


@then(u'токен содержит поле role_name, равное значению role_name, переданому в Запросе')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then токен содержит поле role_name, равное значению role_name, переданому в Запросе')

@when(u'Клиент вызывает GenerateToken() rpc с некорректным значением роли')
def step_impl(context):
    raise NotImplementedError(u'STEP: When Клиент вызывает GenerateToken() rpc с некорректным значением роли')

@then(u'Сервис отправляет Ответ со статусом INVALID_ARGUMENT')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Сервис отправляет Ответ со статусом INVALID_ARGUMENT')


@then(u'Ответ содержит поле token=""')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Ответ содержит поле token=""')
