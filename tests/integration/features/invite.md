# Invite

## Клиент вызывает GenerateToken() rpc со значением роли

"student"/"council_member"/"admin"

_When_ Клиент вызывает GenerateToken() rpc

_And_ Запрос имеет role_name="student"/"council_member"/"admin"

_Then_ Сервис отправляет Ответ со статусом OK

_And_ Ответ содержит поле token, содержащее корректный base64 закодированный JWT-токен

_And_ токен должен быть подписан приватным ключом приложения

_And_ токен содержит поле role_name, равное значению role_name, переданому в Запросе.

## Клиент вызывает GenerateToken() rpc с некорректным значением роли

_When_ Клиент вызывает GenerateToken() rpc

_And_ Запрос имеет role_name="plain"

_Then_ Сервис отправляет Ответ со статусом INVALID_ARGUMENT

_And_ Ответ содержит поле token="".

## Клиент вызывает UpdateUser() rpc для существующего пользователя

_Given_ в базе есть пользователь c user_id=3

_And_ пользователь имеет role_name="student"

_When_ Клиент вызывает UpdateUser() rpc

_And_ Запрос имеет user_id=3

_And_ role_name="council_member"

_Then_ Сервис отправляет Ответ со статусом OK

_And_ Ответ содержит информацию о пользователе с user_id=3

_And_ role_name="council_member"

_And_ в базе у пользователя с user_id=3 устанавливается значение поля role_name="council_member".