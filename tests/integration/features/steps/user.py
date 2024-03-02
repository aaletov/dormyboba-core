from behave import given, when, then

@when(u'Клиент вызывает UpdateUser() rpc с запросом')
def step_impl(context):
    raise NotImplementedError(u'STEP: When Клиент вызывает UpdateUser() rpc с запросом')


@then(u'Ответ содержит информацию о пользователе')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Ответ содержит информацию о пользователе')


@given(u'в базе не содержится пользователей')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given в базе не содержится пользователей')


@then(u'Ответ является пустым сообщением типа UpdateUserResponse')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Ответ является пустым сообщением типа UpdateUserResponse')


@given(u'в базе содержится информация о пользователе')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given в базе содержится информация о пользователе')


@when(u'Клиент вызывает GetUserById() rpc с user_id = 3')
def step_impl(context):
    raise NotImplementedError(u'STEP: When Клиент вызывает GetUserById() rpc с user_id = 3')


@then(u'Ответ является пустым сообщением типа GetUserByIdResponse')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Ответ является пустым сообщением типа GetUserByIdResponse')