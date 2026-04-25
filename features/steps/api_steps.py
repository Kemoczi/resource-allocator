# -- FILE: features/steps/api_steps.py
import requests
from behave import given, when, then


BASE_URL = "http://127.0.0.1:8001"


@given('assignment request contains field "{field}" with value "{value}"')
def step_assignment_request_contains_location(context, field, value):
    context.payload = {
        field: value
    }


@when('user sends POST request to "{endpoint}"')
def step_user_sends_assignment_request(context, endpoint):
    context.response = requests.post(
        f"{BASE_URL}{endpoint}",
        json=context.payload,
        timeout=2
    )
    context.data = context.response.json()


@then("response status code is {expected_status:d}")
def step_response_status_code_is(context, expected_status):
    assert context.response.status_code == expected_status


@then('returned resource has field "{field}" with value "{expected_value}"')
def step_returned_resource_has_location(context, field, expected_value):
    assert context.data[field] == expected_value


@then("returned resource is marked as assigned")
def step_returned_resource_is_marked_as_assigned(context):
    assert context.data["assigned"] is True

