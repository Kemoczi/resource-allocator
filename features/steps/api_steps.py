# -- FILE: features/steps/api_steps.py
import requests
from behave import given, when, then


BASE_URL = "http://127.0.0.1:8001"


@given("assignment request is empty")
def step_assignment_request_is_empty(context):
    context.payload = {}


@given('User sends GET request to root endpoint')
def step_user_sends_get_to_root(context):
    context.response = requests.get(BASE_URL)


@given("assignment request contains:")
def step_assignment_request_contains_table(context):
    context.payload = {}

    for row in context.table:
        context.payload[row["field"]] = row["value"]


@given('assignment request contains field "{field}" with value "{value}"')
def step_assignment_request_contains_location(context, field, value):
    context.payload = {
        field: value
    }


@given('all resources matching location "{location}" are already assigned')
def step_assign_all_resources(context, location):
    payload = {"location": location}

    while True:
        context.response = requests.post(
            f"{BASE_URL}/resources/assign-interface",
            json=payload,
            timeout=2
        )
        if context.response.status_code == 404:
            break
        assert context.response.status_code == 200
    context.payload = payload


@when('user sends POST request to "{endpoint}"')
def step_user_sends_assignment_request(context, endpoint):
    context.response = requests.post(
        f"{BASE_URL}{endpoint}",
        json=context.payload,
        timeout=2
    )
    context.data = context.response.json()


@when('user sends GET request to "{endpoint}"')
def step_user_sends_get_resources(context, endpoint):
    context.response = requests.get(
        f"{BASE_URL}{endpoint}",
        timeout=2
    )
    context.data = context.response.json()


@then('message is "Hello, this is resource allocator!"')
def step_message_is(context):
    assert context.response.json() == {"message": "Hello, this is resource allocator!"}


@then("response status code is {expected_status:d}")
def step_response_status_code_is(context, expected_status):
    assert context.response.status_code == expected_status


@then('returned resource has field "{field}" with value "{expected_value}"')
def step_returned_resource_has_location(context, field, expected_value):
    assert context.data[field] == expected_value


@then("returned resource is marked as assigned")
def step_returned_resource_is_marked_as_assigned(context):
    assert context.data["assigned"] is True


@then("length of returned list is {length:d}")
def step_check_list_len(context, length):
    assert len(context.data) == length


@then('response detail is "{expected_detail}"')
def step_response_detail_is(context, expected_detail):
    assert context.data == {"detail": expected_detail}


@then("response detail is")
def step_response_detail_is_multiline(context):
    assert context.data == {"detail": context.text}
