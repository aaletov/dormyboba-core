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

use_step_matcher("re")

@when(u'Клиент вызывает GetAllInstitutes\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(
        context,
        stub.GetAllInstitutes,
        Empty(),
    )

@then(u'Ответ содержит массив с единственным значением института')
def step_impl(context: behave_runner.Context):
    res: apiv1.GetAllInstitutesResponse = context.response
    assert len(res.institutes) == 1
    institute = res.institutes[0]
    spec = common.Institute(**(json.loads(context.text)[0]))

    assert spec.institute_id == institute.institute_id
    assert spec.institute_name == institute.institute_name

@given(u'в базе не содержится информации об институтах')
def step_impl(context: behave_runner.Context):
    pass

from pydantic import BaseModel

class GetInstituteByNameRequest(BaseModel):
    institute_name: str

    def to_api(self) -> apiv1.GetInstituteByNameRequest:
        return apiv1.GetInstituteByNameRequest(institute_name=self.institute_name)

@when(u'Клиент вызывает GetInstituteByName\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    spec = GetInstituteByNameRequest(**json.loads(context.text))

    await do_rpc(
        context,
        stub.GetInstituteByName,
        spec.to_api()
    )

@then(u'Ответ содержит информацию об институте')
def step_impl(context: behave_runner.Context):
    res: apiv1.GetInstituteByNameResponse = context.response
    spec = common.Institute(**json.loads(context.text))
    assert spec.institute_id == res.institute.institute_id
    assert spec.institute_name == res.institute.institute_name
