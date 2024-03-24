Feature: User

  Scenario: Клиент вызывает UpdateUser() rpc для существующего пользователя
    Given в базе есть роль "student"
    """
    {
      "role_id": 1,
      "role_name": "student"
    }
    """
    And в базе есть роль "council_member"
    """
    {
      "role_id": 2,
      "role_name": "council_member"
    }
    """
    And в базе есть пользователь "A" с ролью "student"
    """
    {
      "user_id": 3,
      "role": {
        "role_id": 1,
        "role_name": "student"
      }
    }
    """
    When Клиент вызывает UpdateUser() rpc для пользователя "A" c ролью "council_member"
    """
    {
      "user_id": 3,
      "role": {
        "role_id": 2,
        "role_name": "council_member"
      }
    }
    """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию о пользователе
    """
    {
      "user_id": 3,
      "role": {
        "role_id": 2,
        "role_name": "council_member"
      }
    }
    """

  Scenario: Клиент вызывает UpdateUser() rpc для несуществующего пользователя
    Given в базе не содержится пользователей
    When Клиент вызывает UpdateUser() rpc для пользователя "A"
    """
    {
      "user_id": 3,
      "role": {
        "role_id": 2,
        "role_name": "council_member"
      }
    }
    """
    Then Сервис отправляет Ответ со статусом INVALID_ARGUMENT

  Scenario: Клиент вызывает GetUserById() rpc для существующего пользователя
    Given в базе есть роль "student"
    """
    {
      "role_id": 1,
      "role_name": "student"
    }
    """
    And в базе есть пользователь "A" с ролью "student"
    """
    {
      "user_id": 3,
      "role": {
        "role_id": 1,
        "role_name": "student"
      }
    }
    """
    When Клиент вызывает GetUserById() rpc с идентификатором пользователя "A"
    """
    {
      "user_id": 3
    }
    """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию о пользователе
    """
    {
      "user_id": 3,
      "role": {
        "role_id": 1,
        "role_name": "student"
      }
    }
    """

  Scenario: Клиент вызывает GetUserById() rpc для несуществующего пользователя
    Given в базе не содержится пользователей
    When Клиент вызывает GetUserById() rpc с идентификатором пользователя "A"
    """
    {
      "user_id": 3
    }
    """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит пустое поле "user"
