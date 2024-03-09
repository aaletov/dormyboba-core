import behave.runner as behave_runner
from behave import given, when, then

@when(u'Клиент вызывает CreateMailing() rpc с запросом')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: When Клиент вызывает CreateMailing() rpc с запросом')


@then(u'Ответ содержит информацию о простой рассылке')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Then Ответ содержит информацию о простой рассылке')


@then(u'Ответ содержит информацию об отложенной рассылке')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Then Ответ содержит информацию об отложенной рассылке')


@then(u'Ответ является пустым сообщением типа CreateMailingResponse')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Then Ответ является пустым сообщением типа CreateMailingResponse')
