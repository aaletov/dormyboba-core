Feature: Academic Type

  Scenario: Клиент вызывает GetAllAcademicTypes() rpc при наличии одного типа академ. программы
    Given в базе есть тип академ. программы "Бакалавриат"
    """
    {
      "type_id": 3,
      "type_name": "Бакалавриат"
    }
    """
    When Клиент вызывает GetAllAcademicTypes() rpc
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит массив с единственным значением типа академ. программы
    """
    [
      {
        "type_id": 3,
        "type_name": "Бакалавриат"
      }
    ]
    """

  Scenario: Клиент вызывает GetAllAcademicTypes() rpc при отсутствии институтов
    Given в базе не содержится информации о типах академ. программ
    When Клиент вызывает GetAllAcademicTypes() rpc
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит пустой массив в поле "academic_types"
    """
    []
    """

  Scenario: Клиент вызывает GetAcademicTypeByName() rpc для существующего типа академ. программы
    Given в базе есть тип академ. программы "Бакалавриат"
    """
    {
      "type_id": 3,
      "type_name": "Бакалавриат"
    }
    """
    When Клиент вызывает GetAcademicTypeByName() rpc для названия типа "Бакалавриат"
    """
    {
      "type_name": "Бакалавриат"
    }
    """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию о типе академ. программы
    """
    {
      "type_id": 3,
      "type_name": "Бакалавриат"
    }
    """