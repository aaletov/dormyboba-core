import behave.runner as behave_runner
from behave import given, when, then

@given(u'в базе содержится информация об одном типе академ. программы')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Given в базе содержится информация об одном типе академ. программы')


@when(u'Клиент вызывает GetAllAcademicTypes() rpc')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: When Клиент вызывает GetAllAcademicTypes() rpc')


@then(u'Ответ содержит массив с единственным значением типа академ. программы')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Then Ответ содержит массив с единственным значением типа академ. программы')


@given(u'в базе не содержится информации о типах академ. программ')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Given в базе не содержится информации о типах академ. программ')


@then(u'Ответ содержит пустой массив')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Then Ответ содержит пустой массив')

@when(u'Клиент вызывает GetAcademicTypeByName() rpc с type_name = "Бакалавриат"')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: When Клиент вызывает GetAcademicTypeByName() rpc с type_name = "Бакалавриат"')


@then(u'Ответ содержит информацию о типе академ. программы')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Then Ответ содержит информацию о типе академ. программы')
