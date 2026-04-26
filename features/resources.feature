Feature: Resource inventory API

  Scenario: Test root endpoint
    When user sends GET request to "/"
    Then response status code is 200
    And message is "Hello, this is resource allocator!"

  Scenario: Test resources list
    When user sends GET request to "/resources/"
    Then response status code is 200
    And length of returned list is 10