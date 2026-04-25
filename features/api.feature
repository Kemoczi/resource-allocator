# -- FILE: features/api.feature
Feature: Resource allocation API

  Scenario Outline: Assign resource by single parameter
    Given assignment request contains field "<field>" with value "<value>"
    When user sends POST request to "/resources/assign-interface"
    Then response status code is 200
    And returned resource has field "<field>" with value "<value>"
    And returned resource is marked as assigned

    Examples:
      | field     | value      |
      | location  | London     |
      | phy_speed | 10G        |
      | optics    | 10GBASE-LR |