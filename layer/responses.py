import os

CLIENT_URLS = os.environ["CLIENT_URLS"].split(",")

GET_HEADER = {
    # "Access-Control-Allow-Origin": CLIENT_URL,
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN,Authorization",
    "Access-Control-Allow-Credentials": "true",
}

POST_HEADER = {
    # "Access-Control-Allow-Origin": CLIENT_URL,
    "Access-Control-Allow-Methods": "POST",
    "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN,Authorization",
    "Access-Control-Allow-Credentials": "true",
}

PUT_HEADER = {
    # "Access-Control-Allow-Origin": CLIENT_URL,
    "Access-Control-Allow-Methods": "PUT",
    "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN,Authorization",
    "Access-Control-Allow-Credentials": "true",
}

DELETE_HEADER = {
    # "Access-Control-Allow-Origin": CLIENT_URL,
    "Access-Control-Allow-Methods": "DELETE",
    "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN,Authorization",
    "Access-Control-Allow-Credentials": "true",
}


def send_response(status_code, body, header, client_url):
    if client_url in CLIENT_URLS:
        header["Access-Control-Allow-Origin"] = client_url
    else:
        header["Access-Control-Allow-Origin"] = CLIENT_URLS[0]
    return {
        "statusCode": status_code,
        "body": body,
        "headers": header,
    }


def get_response(status_code, body, client_url):
    return send_response(status_code, body, GET_HEADER, client_url)


def post_response(status_code, body, client_url):
    return send_response(status_code, body, POST_HEADER, client_url)


def put_response(status_code, body, client_url):
    return send_response(status_code, body, PUT_HEADER, client_url)


def delete_response(status_code, body, client_url):
    return send_response(status_code, body, DELETE_HEADER, client_url)
