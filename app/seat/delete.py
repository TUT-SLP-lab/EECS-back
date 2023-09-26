import datetime

from responses import delete_response
from table_utils import DynamoDBError, delete_desk_user, json_dumps, qa_table


def lambda_handler(event, context):
    ppm = event.get("pathParameters", {})
    if ppm is None:
        return delete_response(400, "Bad Request: Invalid path parameters")

    desk_id = ppm.get("desk_id", None)
    try:
        delete_desk_user(desk_id)
    except DynamoDBError as e:
        return delete_response(500, f"Internal Server Error: DynamoDB Error: {e}")
    except IndexError as e:
        return delete_response(404, f"Not Found: {e}")
    return delete_response(200, json_dumps(delete_desk_user(desk_id)))
