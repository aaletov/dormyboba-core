import json
import datetime
import behave.runner as behave_runner
from behave import given, when, then
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from google.protobuf.timestamp_pb2 import Timestamp
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

from pydantic import BaseModel

class DormybobaRole(BaseModel):
    role_id: int
    role_name: str

    def to_model(self) -> model.DormybobaRole:
        return model.DormybobaRole(role_id=self.role_id, role_name=self.role_name)

@given(u'В базе есть роль "{role}"')
def step_impl(context: behave_runner.Context, role: str):
    spec = DormybobaRole(**json.loads(context.text))
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        session.add(spec.to_model())

def dt_to_timestamp(dt: datetime.datetime | None) -> Timestamp:
    if dt is None:
        return None
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp
