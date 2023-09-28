from datetime import datetime
import jwt

from boto3.dynamodb.conditions import Key
from responses import put_response
from table_utils import (
    DynamoDBError,
    delete_desk_user,
    desk_table,
    get_items,
    json_dumps,
    put_item,
)


def lambda_handler(event, context):
    ppm = event.get("pathParameters", {})
    if ppm is None:
        return put_response(400, "Bad Request: Invalid path parameters")
    desk_id = ppm.get("desk_id", None)
    token = event.get("headers").get("Authorization")
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
    except Exception as e:
        return put_response(500, f"Internal Server Error: {e}")

    username = payload["name"]
    email = payload["email"]

    # 他の机に名前がある場合 -> 名前とEmailを削除
    try:
        index_name = "EmailIndex"
        expr = Key("email").eq(email)
        item = get_items(desk_table, index_name, expr)[0]
        delete_desk_id = item["desk_id"]

        try:
            delete_desk_user(delete_desk_id)
        except DynamoDBError as e:
            return put_response(500, f"Internal Server Error: DynamoDB Error: {e}")
        except IndexError as e:
            return put_response(404, f"Not Found: {e}")
        except Exception as e:
            return put_response(500, f"Internal Server Error: {e}")
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
        response = put_item(desk_table, "desk_id", desk_id, expr, update_object)
    except DynamoDBError as e:
        return put_response(500, f"Internal Server Error: DynamoDB Error: {e}")
    except IndexError as e:
        return put_response(404, f"Not Found: {e}")
    except Exception as e:
        return put_response(500, f"Internal Server Error: {e}")

    return put_response(200, json_dumps(response))
