from controller import sanitise
from util.properties import AppProperties
from util.validator import is_valid_payload

import functions_framework
from json import load


@functions_framework.http
def app(request):
    properties = AppProperties("resources/application.properties")

    with open(properties.payload_schema) as file:
        payload_schema = load(file)

    payload = request.get_data(as_text=True)

    if not is_valid_payload(payload, request.get_json()):
        print("Invlaid payload")
        return "Missing requestId", 422
    else:
        request_id = request.get_json().get("requestId")
        print(f"Sanitising payload with requestId: {request_id}")

    with open(properties.inspect_config) as file:
        inspect_config = load(file)

    with open(properties.tags_file) as file:
        tags = load(file)

    return sanitise(
        properties.project,
        inspect_config,
        payload,
        tags
    )
