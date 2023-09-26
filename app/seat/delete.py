import datetime
from table_utils import DynamoDBError, put_item, qa_table, json_dumps
from responses import delete_response

def lambda_handler(event, context):
    ppm = event.get("pathParameters", {})
    if ppm is None:
        return delete_response(400, "Bad Request: Invalid path parameters")

    desk_id = ppm.get("desk_id", None)
    expr = ", ".join(
        [
            "SET updated_at=:updated_at",
            "username=:username",
            "email=:email",
        ]
    )

    update_object = {
        ":updated_at": datetime.now().isoformat(),
        ":username": None,
        ":email": None,
    }

    try:
        response = put_item(qa_table, "desk_id", desk_id, expr, update_object)
    except DynamoDBError as e:
        return delete_response(500, f"Internal Server Error: DynamoDB Error: {e}")
    except IndexError as e:
        return delete_response(404, f"Not Found: {e}")


    return delete_response(200, json_dumps(response))
