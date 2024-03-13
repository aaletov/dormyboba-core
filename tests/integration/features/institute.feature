Feature: Institute

  Scenario: Клиент вызывает GetAllInstitutes() rpc при наличии одного института
    Given в базе содержится информация об одном институте
    """
    {
      "institute_id": 3,
      "institute_name": "ИКНТ"
    }
    """
    When Клиент вызывает GetAllInstitutes() rpc
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит массив с единственным значением института
      """
      [
        {
          "institute_id": 3,
          "institute_name": "ИКНТ"
        }
      ]
      """

  Scenario: Клиент вызывает GetAllInstitutes() rpc при отсутствии институтов
    Given в базе не содержится информации об институтах
    When Клиент вызывает GetAllInstitutes() rpc
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит пустой массив
      """
      []
      """

  Scenario: Клиент вызывает GetInstituteByName() rpc для существующего института
    Given в базе содержится информация об одном институте
    """
    {
      "institute_id": 3,
      "institute_name": "ИКНТ"
    }
    """
    When Клиент вызывает GetInstituteByName() rpc с institute_name = "ИКНТ"
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию об институте
    """
      {
        "institute_id": 3,
        "institute_name": "ИКНТ"
      }
    """
