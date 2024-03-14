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

def parse_academic_type(context: behave_runner. Context) -> dict:
    return json.loads(context.text)

@given(u'в базе содержится информация об одном типе академ. программы')
def step_impl(context: behave_runner.Context):
    given_academic_type = parse_academic_type(context)
    with Session(context.engine) as session, session.begin():
        academic_types = [
            model.AcademicType(
                type_id=given_academic_type["type_id"],
                type_name=given_academic_type["type_name"],
            ),
        ]
        session.add_all(academic_types)

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
    then_academic_type = parse_academic_type(context)
    assert then_academic_type["type_id"] == academic_type.type_id
    assert then_academic_type["type_name"] == academic_type.type_name

@given(u'в базе не содержится информации о типах академ. программ')
def step_impl(context: behave_runner.Context):
    pass

@when(u'Клиент вызывает GetAcademicTypeByName() rpc с type_name = "Бакалавриат"')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(
        context,
        stub.GetAcademicTypeByName,
        apiv1.GetAcademicTypeByNameRequest(
            type_name="Бакалавриат",
        ),
    )

@then(u'Ответ содержит информацию о типе академ. программы')
def step_impl(context: behave_runner.Context):
    res: apiv1.GetAcademicTypeByNameResponse = context.response
    then_academic_type = parse_academic_type(context)
    assert then_academic_type["type_id"] == res.academic_type.type_id
    assert then_academic_type["type_name"] == res.academic_type.type_name
