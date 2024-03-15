import json
import datetime
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

def parse_mailing(context: behave_runner. Context) -> dict:
    return json.loads(context.text)

@when(u'Клиент вызывает CreateMailing() rpc с запросом')
@async_run_until_complete
async def step_impl(context: behave_runner.Context):
    when_mailing = parse_mailing(context)
    when_at = None
    if "at" in when_mailing:
        when_at = datetime.datetime.strptime(when_mailing["at"], '%Y-%m-%d %H:%M:%S.%f')
    stub: apiv1grpc.DormybobaCoreStub = context.stub
    await do_rpc(
        context,
        stub.CreateMailing,
        apiv1.CreateMailingRequest(
            apiv1.Mailing(
                theme=when_mailing["theme"],
                mailing_text=when_mailing["mailing_text"],
                at=when_at,
            ),
        ),
    )


@then(u'Ответ содержит информацию о простой рассылке')
def step_impl(context: behave_runner.Context):
    then_mailing = parse_mailing(context)
    res: apiv1.CreateMailingResponse = context.response
    assert res.mailing.HasField("mailing_id")
    assert then_mailing["theme"] == res.mailing.theme
    assert then_mailing["mailing_text"] == res.mailing.mailing_text

@then(u'Ответ содержит информацию об отложенной рассылке')
def step_impl(context: behave_runner.Context):
    then_mailing = parse_mailing(context)
    res: apiv1.CreateMailingResponse = context.response
    assert res.mailing.HasField("mailing_id")
    assert then_mailing["theme"] == res.mailing.theme
    assert then_mailing["mailing_text"] == res.mailing.mailing_text
    then_at = datetime.datetime.strptime(then_mailing["at"], '%Y-%m-%d %H:%M:%S.%f')

    assert then_at == res.mailing.at
