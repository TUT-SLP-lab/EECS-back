from table_utils import get_all_items, qa_table, json_dumps
from responses import get_response

def lambda_handler(event, context):
    try:
        response = get_all_items(qa_table)
    except Exception as e:
        return get_response(500, json_dumps(e))

    return get_response(200, json_dumps(response))
