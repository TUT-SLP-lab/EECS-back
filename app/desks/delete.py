from table_utils import DynamoDBError, delete_item, qa_table, json_dumps
from responses import delete_response

def lambda_handler(event, context):
    ppm = event.get("pathParameters")
    if ppm is None:
        return delete_response(400, "Bad Request: Invalid path parameters")
    desk_id = ppm.get("desk_id")
    try:
        delete_item(qa_table, "desk_id", desk_id)
    except DynamoDBError as e:
        return delete_response(500, f"Internal Server Error: DynamoDB Error: {e}")

    return delete_response(200, json_dumps({"message": f"Deleted desk with ID: {desk_id}"}))
