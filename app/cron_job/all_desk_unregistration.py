from responses import delete_response
from table_utils import (
    DynamoDBError,
    delete_desk_user,
    desk_table,
    get_all_items,
    json_dumps,
)

import os

CLIENT_URLS = os.environ["CLIENT_URLS"].split(",")


def lambda_handler(event, context):
    origin = event.get("headers", {}).get("Origin", CLIENT_URLS[0])
    try:
        for desk in get_all_items(desk_table):
            desk_id = desk["desk_id"]
            delete_desk_user(desk_id)
    except DynamoDBError as e:
        return delete_response(500, f"Internal Server Error: DynamoDB Error: {e}", origin)
    except IndexError as e:
        return delete_response(404, f"Not Found: {e}", origin)
    return delete_response(200, json_dumps("OK"), origin)
