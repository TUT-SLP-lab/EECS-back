import datetime
import json
import base64
from boto3.dynamodb.conditions import Key

from table_utils import DynamoDBError, get_item, put_item, qa_table, json_dumps
from responses import put_response

def lambda_handler(event, context):
    ppm = event.get("pathParameters", {})
    if ppm is None:
        return put_response(400, "Bad Request: Invalid path parameters")
    desk_id = ppm.get("desk_id", None)
    token = event.get("headers").get("Authorization")
    payload=base64.b64decode(token)
    payload=json.loads(payload)

    username = payload
    email =

    # 他の机に名前がある場合 -> 名前とEmailを削除
    try:
        item = get_item(qa_table, "email", email)
        delete_desk_id = item["Item"]["desk_id"]

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
            put_item(qa_table, "desk_id", delete_desk_id, expr, update_object)
        except DynamoDBError as e:
            return put_response(500, f"Internal Server Error: DynamoDB Error: {e}")
        except IndexError as e:
            return put_response(404, f"Not Found: {e}")
    except IndexError:
        pass


    expr = ", ".join(
        [
            "SET updated_at=:updated_at",
            "username=:username",
            "email=:email",
        ]
    )

    update_object = {
        ":updated_at": datetime.now().isoformat(),
        ":username": username,
        ":email": email,
    }

    try:
        response = put_item(qa_table, "desk_id", desk_id, expr, update_object)
    except DynamoDBError as e:
        return put_response(500, f"Internal Server Error: DynamoDB Error: {e}")
    except IndexError as e:
        return put_response(404, f"Not Found: {e}")

    return put_response(200, json_dumps(response))
