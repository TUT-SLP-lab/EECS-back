import json
from datetime import datetime

from responses import put_response
from table_utils import (
    DynamoDBError,
    desk_table,
    json_dumps,
    put_item,
)


def update_desk(desk: dict) -> dict:
    desk_id = desk.get()
    room = desk.get("room", None)
    email = desk.get("email", None)
    username = desk.get("username", None)
    position = desk.get("position", None)
    size = desk.get("size", None)

    expr = ", ".join(
        [
            "SET room=:room",
            "email=:email",
            "username=:username",
            "position=:position",
            "size=:size",
            "updated_at=:updated_at",
        ]
    )

    update_object = {
        ":room": room,
        ":email": email,
        ":username": username,
        ":position": position,
        ":size": size,
        ":updated_at": datetime.now().isoformat(),
    }

    try:
        desk = put_item(desk_table, "desk_id", desk_id, expr, update_object)
    except DynamoDBError as e:
        return put_response(500, f"Internal Server Error: DynamoDB Error: {e}")
    except IndexError as e:
        return put_response(404, f"Not Found: {e}")

    return desk


def lambda_handler(event, context):
    desk_list = list()
    body = json.loads(event.get("body", "{}"))
    if body is None:
        return put_response(400, "Bad Request: Invalid body")
    for desk in body:
        desk_list.append(update_desk(desk))
    return put_response(200, json_dumps(desk_list))
