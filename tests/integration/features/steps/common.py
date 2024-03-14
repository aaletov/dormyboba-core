import behave.runner as behave_runner
from behave import given, when, then
from sqlalchemy import Engine
from sqlalchemy.orm import Session
import dormyboba_api.v1api_pb2 as apiv1
import dormyboba_core.model as model
import grpc

@then(u'Сервис отправляет Ответ со статусом OK')
def step_impl(context: behave_runner.Context):
    assert context.status == grpc.StatusCode.OK

@then(u'Ответ содержит пустой массив в поле "{field}"')
def step_impl(context: behave_runner.Context, field: str):
    res: apiv1.GetAllAcademicTypesResponse = context.response
    assert len(getattr(res, field)) == 0

def add_standard_roles(context: behave_runner.Context):
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        roles = [
            model.DormybobaRole(role_id=1, role_name="student"),
            model.DormybobaRole(role_id=2, role_name="council_member"),
            model.DormybobaRole(role_id=3, role_name="admin"),
        ]
        session.add_all(roles)