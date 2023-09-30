from responses import get_response
from table_utils import desk_table, get_all_items, json_dumps


def lambda_handler(event, context):
    origin = event.get("headers").get("Origin")
    try:
        response = get_all_items(desk_table)
    except Exception as e:
        return get_response(500, json_dumps(e), origin)

    return get_response(200, json_dumps(response), origin)
