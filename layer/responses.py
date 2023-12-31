import os

CLIENT_URL = os.environ["CLIENT_URL"]

GET_HEADER = {
    "Access-Control-Allow-Origin": CLIENT_URL,
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN,Authorization",
    "Access-Control-Allow-Credentials": "true",
}

POST_HEADER = {
    "Access-Control-Allow-Origin": CLIENT_URL,
    "Access-Control-Allow-Methods": "POST",
    "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN,Authorization",
    "Access-Control-Allow-Credentials": "true",
}

PUT_HEADER = {
    "Access-Control-Allow-Origin": CLIENT_URL,
    "Access-Control-Allow-Methods": "PUT",
    "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN,Authorization",
    "Access-Control-Allow-Credentials": "true",
}

DELETE_HEADER = {
    "Access-Control-Allow-Origin": CLIENT_URL,
    "Access-Control-Allow-Methods": "DELETE",
    "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN,Authorization",
    "Access-Control-Allow-Credentials": "true",
}


def send_response(status_code, body, header):
    return {
        "statusCode": status_code,
        "body": body,
        "headers": header,
    }


def get_response(status_code, body):
    return send_response(status_code, body, GET_HEADER)


def post_response(status_code, body):
    return send_response(status_code, body, POST_HEADER)


def put_response(status_code, body):
    return send_response(status_code, body, PUT_HEADER)


def delete_response(status_code, body):
    return send_response(status_code, body, DELETE_HEADER)
