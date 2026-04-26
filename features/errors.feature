Feature: Resource assignment error handling

  Scenario: Assignment request has no matching resource
    Given assignment request contains:
      | field    | value    |
      | location | Olesnica |
    When user sends POST request to "/resources/assign-interface"
    Then response status code is 404
    And response detail is "No resources with specified parameters available"

  Scenario: Assignment request contains invalid field
    Given assignment request contains:
      | field | value |
      | speed | 10G   |
    When user sends POST request to "/resources/assign-interface"
    Then response status code is 422
    And response detail is "Error - Invalid request body. Check field names."

  Scenario: Assignment request is empty
    Given assignment request is empty
    When user sends POST request to "/resources/assign-interface"
    Then response status code is 400
    And response detail is "You must provide at least one resource parameter"