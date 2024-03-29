from typing import Optional
import json
import datetime
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

from pydantic import BaseModel

class Mailing(BaseModel):
    mailing_id: Optional[int] = None
    theme: Optional[str] = None
    mailing_text: str
    at: Optional[str] = None

    def to_api(self) -> apiv1.Mailing:
        dt_at = None
        if self.at is not None:
            dt_at = datetime.datetime.strptime(self.at, '%Y-%m-%d %H:%M:%S.%f')
        return apiv1.Mailing(
            mailing_id=self.mailing_id,
            theme=self.theme,
            mailing_text=self.mailing_text,
            at=common.dt_to_timestamp(dt_at),
        )

use_step_matcher("re")

@when(u'Клиент вызывает CreateMailing\(\) rpc(?P<anything>.*)')
@async_run_until_complete
async def step_impl(context: behave_runner.Context, anything: str):
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    spec = Mailing(**json.loads(context.text))
    await do_rpc(
        context,
        stub.CreateMailing,
        apiv1.CreateMailingRequest(
            mailing=spec.to_api()
        ),
    )

@then(u'Ответ содержит информацию о созданной рассылке')
def step_impl(context: behave_runner.Context):
    res: apiv1.CreateMailingResponse = context.response
    api_spec = Mailing(**json.loads(context.text)).to_api()
    assert res.mailing.HasField("mailing_id")
    assert api_spec.theme == res.mailing.theme
    assert api_spec.mailing_text == res.mailing.mailing_text
    assert not(api_spec.at is not None) or (api_spec.at == res.mailing.at)
