from behave import given, when, then

@given(u'в базе содержится информация об одном институте')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given в базе содержится информация об одном институте')


@when(u'Клиент вызывает GetAllInstitutes() rpc')
def step_impl(context):
    raise NotImplementedError(u'STEP: When Клиент вызывает GetAllInstitutes() rpc')


@then(u'Ответ содержит массив с единственным значением института')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Ответ содержит массив с единственным значением института')


@given(u'в базе не содержится информации об институтах')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given в базе не содержится информации об институтах')


@when(u'Клиент вызывает GetInstituteByName() rpc с institute_name = "ИКНТ"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When Клиент вызывает GetInstituteByName() rpc с institute_name = "ИКНТ"')


@then(u'Ответ содержит информацию об институте')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Ответ содержит информацию об институте')
