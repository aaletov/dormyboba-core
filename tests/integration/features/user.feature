Feature: User

  Scenario: Клиент вызывает UpdateUser() rpc для существующего пользователя
    Given в базе содержится информация о пользователе
      """
      {
        "user_id": 3,
        "role_name": "student"
      }
      """
    When Клиент вызывает UpdateUser() rpc с запросом
      """
      {
        "user_id": 3,
        "role_name": "council_member"
      }
      """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию о пользователе
      """
      {
        "user_id": 3,
        "role_name": "council_member"
      }
      """

  Scenario: Клиент вызывает UpdateUser() rpc для несуществующего пользователя
    Given в базе не содержится пользователей
    When Клиент вызывает UpdateUser() rpc с запросом
      """
      {
        "user_id": 3,
        "role_name": "council_member"
      }
      """
    Then Сервис отправляет Ответ со статусом INVALID_ARGUMENT

  Scenario: Клиент вызывает GetUserById() rpc для существующего пользователя
    Given в базе содержится информация о пользователе
    """
    {
      "user_id": 3,
      "role_name": "council_member"
    }
    """
    When Клиент вызывает GetUserById() rpc с user_id = 3
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию о пользователе
    """
    {
      "user_id": 3,
      "role_name": "council_member"
    }
    """

  Scenario: Клиент вызывает GetUserById() rpc для несуществующего пользователя
    Given в базе не содержится пользователей
    When Клиент вызывает GetUserById() rpc с user_id = 3
    Then Сервис отправляет Ответ со статусом INVALID_ARGUMENT
