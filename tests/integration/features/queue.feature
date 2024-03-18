Feature: Queue

  Scenario: Клиент вызывает CreateQueue() rpc и создаёт простую очередь
    When Клиент вызывает CreateQueue() rpc с запросом
    """
    {
      "title": "Название очереди",
      "open": "2024-03-02 20:05:25.231189"
    }
    """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию об очереди
    """
    {
      "queue_id": "{queue_id}",
      "title": "Название очереди",
      "open": "2024-03-02 20:05:25.231189",
      "event_generated": false
    }
    """

  Scenario: Клиент вызывает AddPersonToQueue() rpc для пустой очереди
    Given в базе есть очередь "A"
    """
    {
      "queue_id": 3,
      "title": "Название очереди",
      "open": "2024-03-02 20:05:25.231189"
      "event_generated": true
    }
    """
    And в базе есть роль "student"
    """
    {
      "role_id": 1,
      "role_name": "student"
    }
    """
    And в базе есть пользователь "B" с ролью "student"
    """
    {
      "user_id": 3,
      "role": {
        "role_id": 1,
        "role_name": "student"
      }
    }
    """
    When Клиент вызывает AddPersonToQueue() rpc для очереди "A" и пользователя "B"
    """
    {
      "queue_id": 3,
      "user_id": 4
    }
    """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию о том, что добавленный пользователь является активным пользователем в очереди
    """
    {
      "is_active": true
    }
    """

  Scenario: Клиент вызывает AddPersonToQueue() rpc для непустой очереди и существующего пользователя
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
    And в базе есть пользователь "B" с ролью "student"
    """
    {
      "user_id": 4,
      "role": {
        "role_id": 1,
        "role_name": "student"
      }
    }
    """
    And в базе есть очередь "C", активным пользователем в которой является пользователь "A"
    """
    {
      "queue_id": 3,
      "title": "Название очереди",
      "open": "2024-03-02 20:05:25.231189",
      "event_generated": true,
      "active_user_id": 3
    }
    """
    When Клиент вызывает AddPersonToQueue() rpc для пользователя "B" и очереди "C"
    """
    {
      "queue_id": 3,
      "user_id": 4
    }
    """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию о том, что добавленный пользователь не является активным пользователем в очереди
    """
    {
      "is_active": false
    }
    """

  Scenario: Клиент вызывает RemovePersonFromQueue() rpc для существующего пользователя, находящегося в существующей очереди
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
    And в базе есть очередь "B", активным пользователем в которой является пользователь "A"
    """
    {
      "queue_id": 3,
      "title": "Название очереди",
      "open": "2024-03-02 20:05:25.231189",
      "event_generated": true,
      "active_user_id": 3
    }
    """
    When Клиент вызывает RemovePersonFromQueue() rpc для пользователя "A" и очереди "B"
    """
    {
      "queue_id": 3,
      "user_id": 4
    }
    """
    Then Сервис отправляет Ответ со статусом OK

  Scenario: Клиент вызывает PersonCompleteQueue() rpc для пользователя, являющимся активным в данной очереди при отсутствии ожидающих пользователей
    Given в базе есть роль "student"
    """
    {
      "role_id": 1,
      "role_name": "student"
    }
    """
    And в базе есть пользователь "A" с ролью "student" и идентификатором 3
    """
    {
      "user_id": 3,
      "role": {
        "role_id": 1,
        "role_name": "student"
      }
    }
    """
    And в базе есть очередь "B", активным пользователем в которой является пользователь "A"
    """
    {
      "queue_id": 3,
      "title": "Название очереди",
      "open": "2024-03-02 20:05:25.231189"
      "event_generated": true,
      "active_user_id": 3,
    }
    """
    When Клиент вызывает PersonCompleteQueue() rpc для пользователя "A" и очереди "C"
    """
    {
      "queue_id": 3,
      "user_id": 4
    }
    """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию о том, что очередь теперь пуста
    """
    {
      "is_queue_empty": true,
      "active_user_id": null
    }
    """
