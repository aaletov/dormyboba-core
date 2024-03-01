Feature: Invite

  Scenario: Клиент вызывает GenerateToken() rpc со значением роли
  "student"/"council_member"/"admin"
    When Клиент вызывает GenerateToken() rpc
    And Запрос имеет role_name="student"/"council_member"/"admin"
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит поле token, содержащее корректный base64 закодированный JWT-токен
    And токен должен быть подписан приватным ключом приложения
    And токен содержит поле role_name, равное значению role_name, переданому в Запросе

  Scenario: Клиент вызывает GenerateToken() rpc с некорректным значением роли
    When Клиент вызывает GenerateToken() rpc
    And Запрос имеет role_name="plain"
    Then Сервис отправляет Ответ со статусом INVALID_ARGUMENT
    And Ответ содержит поле token=""

  Scenario: Клиент вызывает UpdateUser() rpc для существующего пользователя
    Given в базе есть пользователь c user_id=3
    And пользователь имеет role_name="student"
    When Клиент вызывает UpdateUser() rpc
    And Запрос имеет user_id=3
    And role_name="council_member"
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию о пользователе с user_id=3
    And role_name="council_member"
    And в базе у пользователя с user_id=3 устанавливается значение поля role_name="council_member"