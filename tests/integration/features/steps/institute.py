import json
import behave.runner as behave_runner
from behave.api.async_step import async_run_until_complete
from behave import given, when, then
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from google.protobuf.empty_pb2 import Empty
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_api.v1api_pb2_grpc as apiv1grpc
import dormyboba_core.model as model
from tests.integration.features.steps.wrapper import do_rpc

# Import common steps so decorator will be invoked
import tests.integration.features.steps.common as common

def parse_institute(context: behave_runner. Context) -> dict:
    return json.loads(context.text)

@given(u'в базе содержится информация об одном институте')
def step_impl(context: behave_runner.Context):
    with Session(context.engine) as session, session.begin():
        institutes = [
            model.Institute(institute_id=35, institute_name="ИКНТ"),
        ]
        session.add_all(institutes)

@when(u'Клиент вызывает GetAllInstitutes() rpc')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
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

@given(u'в базе не содержится информации об институтах')
def step_impl(context: behave_runner.Context):
    pass

@when(u'Клиент вызывает GetInstituteByName() rpc с institute_name = "ИКНТ"')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(
        context,
        stub.GetInstituteByName,
        apiv1.GetInstituteByNameRequest(
            institute_name="ИКНТ",
        ),
    )

@then(u'Ответ содержит информацию об институте')
def step_impl(context: behave_runner.Context):
    then_institute = parse_institute(context)
    res: apiv1.GetInstituteByNameResponse = context.response
    assert then_institute["institute_id"] == res.institute.institute_id
    assert then_institute["institute_name"] == res.institute.institute_name
