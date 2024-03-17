Feature: Token

  Scenario: Клиент вызывает GenerateToken() rpc с корректным значением роли
    Given в базе есть роль "student"
    """
    {
      "role_id": 1,
      "role_name": "student"
    }
    """
    When Клиент вызывает GenerateToken() rpc для роли "student"
    """
    {
      "role_name": "student"
    }
    """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит поле token, содержащее корректный base64 закодированный JWT-токен
    And токен должен быть подписан приватным ключом приложения
    And токен содержит поле role_name, равное значению role_name, переданому в Запросе
    """
    {
      "role_name": "student"
    }
    """

  Scenario: Клиент вызывает GenerateToken() rpc с некорректным значением роли
    Given в базе есть роль "student"
    """
    {
      "role_id": 1,
      "role_name": "student"
    }
    """
    When Клиент вызывает GenerateToken() rpc для роли "abobus"
    """
    {
      "role_name": "abobus"
    }
    """
    Then Сервис отправляет Ответ со статусом INVALID_ARGUMENT
