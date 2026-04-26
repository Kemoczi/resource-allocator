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

  Scenario: Assign resource by location, physical speed and optics
    Given assignment request contains:
      | field     | value      |
      | location  | London     |
      | phy_speed | 1G         |
      | optics    | 1GBASE-SR  |
    When user sends POST request to "/resources/assign-interface"
    Then response status code is 200
    And returned resource has field "location" with value "London"
    And returned resource has field "phy_speed" with value "1G"
    And returned resource has field "optics" with value "1GBASE-SR"
    And returned resource is marked as assigned

  Scenario: Cannot assign resource when matching pool is exhausted
    Given all resources matching location "London" are already assigned
    And assignment request contains field "location" with value "London"
    When user sends POST request to "/resources/assign-interface"
    Then response status code is 404
    And response detail is "No resources with specified parameters available"