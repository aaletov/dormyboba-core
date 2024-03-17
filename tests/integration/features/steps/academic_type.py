import json
import behave.runner as behave_runner
from behave.api.async_step import async_run_until_complete
from behave import use_step_matcher, given, when, then
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from google.protobuf.empty_pb2 import Empty
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
import dormyboba_core.model as model
from tests.integration.features.steps.wrapper import do_rpc

# Import common steps so decorator will be invoked
import tests.integration.features.steps.common as common

@when(u'Клиент вызывает GetAllAcademicTypes() rpc')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(
        context,
        stub.GetAllAcademicTypes,
        Empty(),
    )

@then(u'Ответ содержит массив с единственным значением типа академ. программы')
def step_impl(context: behave_runner.Context):
    res: apiv1.GetAllAcademicTypesResponse = context.response
    assert len(res.academic_types) == 1
    academic_type = res.academic_types[0]
    spec = common.AcademicType(**(json.loads(context.text)[0]))
    assert spec.type_id == academic_type.type_id
    assert spec.type_name == academic_type.type_name

@given(u'в базе не содержится информации о типах академ. программ')
def step_impl(context: behave_runner.Context):
    pass

from pydantic import BaseModel

class GetAcademicTypeByNameRequest(BaseModel):
    type_name: str

    def to_api(self) -> apiv1.GetAcademicTypeByNameRequest:
        return apiv1.GetAcademicTypeByNameRequest(type_name=self.type_name)

use_step_matcher("re")

@when(u'Клиент вызывает GetAcademicTypeByName\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    spec = GetAcademicTypeByNameRequest(**json.loads(context.text))
    await do_rpc(
        context,
        stub.GetAcademicTypeByName,
        spec.to_api(),
    )

@then(u'Ответ содержит информацию о типе академ. программы')
def step_impl(context: behave_runner.Context):
    res: apiv1.GetAcademicTypeByNameResponse = context.response
    spec = common.AcademicType(**json.loads(context.text))
    assert spec.type_id == res.academic_type.type_id
    assert spec.type_name == res.academic_type.type_name
