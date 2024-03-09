import behave.runner as behave_runner
from behave import given, when, then

@when(u'Клиент вызывает CreateQueue() rpc с запросом')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: When Клиент вызывает CreateQueue() rpc с запросом')


@then(u'Ответ содержит информацию о простой очереди')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Then Ответ содержит информацию о простой очереди')


@given(u'в базе есть пустая очередь с queue_id = 3')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Given в базе есть пустая очередь с queue_id = 3')


@given(u'в базе есть пользователь с user_id = 4')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Given в базе есть пользователь с user_id = 4')


@when(u'Клиент вызывает AddPersonToQueue() rpc с запросом')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: When Клиент вызывает AddPersonToQueue() rpc с запросом')


@then(u'Ответ содержит информацию о том, что добавленный пользователь является активным пользователем в очереди')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Then Ответ содержит информацию о том, что добавленный пользователь является активным пользователем в очереди')


@given(u'в базе есть непустая очередь с queue_id = 3')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Given в базе есть непустая очередь с queue_id = 3')


@then(u'Ответ содержит информацию о том, что добавленный пользователь не является активным пользователем в очереди')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Then Ответ содержит информацию о том, что добавленный пользователь не является активным пользователем в очереди')


@given(u'в базе есть пользователь с user_id = 4, находящийся в очереди с queue_id = 3')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Given в базе есть пользователь с user_id = 4, находящийся в очереди с queue_id = 3')


@when(u'Клиент вызывает RemovePersonFromQueue() rpc с запросом')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: When Клиент вызывает RemovePersonFromQueue() rpc с запросом')


@given(u'активным пользователем в очереди с queue_id = 3 является пользователь с user_id = 4')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Given активным пользователем в очереди с queue_id = 3 является пользователь с user_id = 4')


@when(u'Клиент вызывает PersonCompleteQueueRequest() rpc с запросом')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: When Клиент вызывает PersonCompleteQueueRequest() rpc с запросом')


@then(u'Ответ содержит информацию о том, что очередь теперь пуста')
def step_impl(context: behave_runner.Context):
    raise NotImplementedError(u'STEP: Then Ответ содержит информацию о том, что очередь теперь пуста')