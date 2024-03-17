import json
import datetime
import behave.runner as behave_runner
from behave import use_step_matcher, given, when, then
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

    def to_api(self) -> apiv1.DormybobaRole:
        return apiv1.DormybobaRole(role_id=self.role_id, role_name=self.role_name)

@given(u'в базе есть роль "{role}"')
def step_impl(context: behave_runner.Context, role: str):
    spec = DormybobaRole(**json.loads(context.text))
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        session.add(spec.to_model())

class DormybobaUser(BaseModel):
    user_id: int
    role: DormybobaRole
    registration_complete: bool = False

    def to_model(self) -> model.DormybobaUser:
        return model.DormybobaUser(
            user_id=self.user_id,
            role_id=self.role.to_model().role_id,
            registration_complete=self.registration_complete,
        )

    def to_api(self) -> apiv1.DormybobaUser:
        return apiv1.DormybobaUser(
            user_id=self.user_id,
            role=self.role.to_api(),
            is_registered=self.registration_complete,
        )

use_step_matcher("re")

@given(u'в базе есть пользователь(?P<anything>.*)')
def step_impl(context: behave_runner.Context, anything: str):
    spec = DormybobaUser(**json.loads(context.text))
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        session.add(spec.to_model())

use_step_matcher("parse")

class AcademicType(BaseModel):
    type_id: int
    type_name: str

    def to_model(self) -> model.AcademicType:
        return model.AcademicType(type_id=self.type_id, type_name=self.type_name)

    def to_api(self) -> apiv1.AcademicType:
        return apiv1.AcademicType(type_id=self.type_id, type_name=self.type_name)

@given(u'в базе есть тип академ. программы "{academic_type_name}"')
def step_impl(context: behave_runner.Context, academic_type_name: str):
    spec = AcademicType(**json.loads(context.text))
    engine: Engine = context.engine
    with Session(engine) as session, session.begin():
        session.add(spec.to_model())

def dt_to_timestamp(dt: datetime.datetime | None) -> Timestamp:
    if dt is None:
        return None
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp
