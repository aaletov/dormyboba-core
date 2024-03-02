Feature: Mailing

  Scenario: Клиент вызывает CreateMailing() rpc и создаёт простую рассылку
    When Клиент вызывает CreateMailing() rpc с запросом
      """
      {
        theme: "Тема рассылки",
        mailing_text: "Текст рассылки"
      }
      """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию о простой рассылке
      """
      {
        mailing_id: {mailing_id},
        theme: "Тема рассылки",
        mailing_text: "Текст рассылки"
      }
      """

  Scenario: Клиент вызывает CreateMailing() rpc и создаёт отложенную рассылку
    When Клиент вызывает CreateMailing() rpc с запросом
      """
      {
        theme: "Тема рассылки",
        mailing_text: "Текст рассылки",
        at: "2024-03-02 20:05:25.231189"
      }
      """
    Then Сервис отправляет Ответ со статусом OK
    And Ответ содержит информацию об отложенной рассылке
      """
      {
        mailing_id: {mailing_id},
        theme: "Тема рассылки",
        mailing_text: "Текст рассылки",
        at: "2024-03-02 20:05:25.231189"
      }
      """

  Scenario: Клиент вызывает CreateMailing() rpc и создаёт отложенную рассылку с некорректным временем
    When Клиент вызывает CreateMailing() rpc с запросом
      """
      {
        theme: "Тема рассылки",
        mailing_text: "Текст рассылки",
        at: "1990-03-02 20:05:25.231189"
      }
      """
    Then Сервис отправляет Ответ со статусом INVALID_ARGUMENT
    And Ответ является пустым сообщением типа CreateMailingResponse
