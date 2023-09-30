from responses import delete_response
from table_utils import DynamoDBError, delete_desk_user, json_dumps


def lambda_handler(event, context):
    origin = event.get("headers").get("Origin")
    ppm = event.get("pathParameters", {})
    if ppm is None:
        return delete_response(400, "Bad Request: Invalid path parameters", origin)

    desk_id = ppm.get("desk_id", None)
    try:
        delete_desk_user(desk_id, origin)
    except DynamoDBError as e:
        return delete_response(500, f"Internal Server Error: DynamoDB Error: {e}", origin)
    except IndexError as e:
        return delete_response(404, f"Not Found: {e}", origin)
    return delete_response(200, json_dumps(delete_desk_user(desk_id)), origin)
