from responses import delete_response
from table_utils import DynamoDBError, delete_item, json_dumps, qa_table


def lambda_handler(event, context):
    origin = event.get("headers").get("Origin")
    ppm = event.get("pathParameters")
    if ppm is None:
        return delete_response(400, "Bad Request: Invalid path parameters", origin)
    desk_id = ppm.get("desk_id")
    try:
        delete_item(qa_table, "desk_id", desk_id)
    except DynamoDBError as e:
        return delete_response(500, f"Internal Server Error: DynamoDB Error: {e}", origin)

    return delete_response(200, json_dumps({"message": f"Deleted desk with ID: {desk_id}"}), origin)
