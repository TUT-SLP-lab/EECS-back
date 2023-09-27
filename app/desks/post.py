import uuid
from datetime import datetime

from responses import post_response
from table_utils import desk_table, json_dumps, post_item


def lambda_handler(event, context):
    ppm = event.get("pathParameters", {})
    if ppm is None:
        return post_response(400, "Bad Request: Invalid path parameters")
    room = ppm.get("room")

    now = datetime.now().isoformat()
    desk_id = str(uuid.uuid4())
    desk = {
        "desk_id": desk_id,
        "room": room,
        "email": " ",
        "username": " ",
        "position": {"x": 100, "y": 100},
        "size": {"x": 120, "y": 70},
        "create_at": now,
        "update_at": now,
    }

    response = post_item(desk_table, desk)
    return post_response(200, json_dumps(response))
