from responses import delete_response
from table_utils import (
    DynamoDBError,
    delete_desk_user,
    desk_table,
    get_all_items,
    json_dumps,
)


def lambda_handler(event, context):
    try:
        for desk in get_all_items(desk_table):
            desk_id = desk["desk_id"]
            delete_desk_user(desk_id)
    except DynamoDBError as e:
        return delete_response(500, f"Internal Server Error: DynamoDB Error: {e}")
    except IndexError as e:
        return delete_response(404, f"Not Found: {e}")
    return delete_response(200, json_dumps("OK"))
