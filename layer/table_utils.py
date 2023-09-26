import datetime
import json
import os

import boto3
from boto3.dynamodb.conditions import Key

PR_NUM = os.environ["PR_NUM"]
QA_TABLE = f"DeskTable-{PR_NUM}"

dynamodb = boto3.resource("dynamodb")
qa_table = dynamodb.Table(QA_TABLE)


def json_dumps(obj):
    return json.dumps(obj, ensure_ascii=False)


def get_all_items(table) -> list:
    """
    テーブルから全てのアイテムを取得する
    Args:
        table (boto3.resource.Table): テーブル
    Returns:
        list: アイテムのリスト
    Raises:
        DynamoDBError: DynamoDBのエラー
    """
    response = table.scan()
    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise DynamoDBError(f"Failed to find {table.name}")
    if "Items" not in response:
        raise IndexError(f"Items of {table.name} are not found")
    return response["Items"]


def get_items(table, index_name: str, expr: Key) -> list:
    """テーブルからアイテムを取得する

    Args:
        table (boto3.resource.Table): テーブル
        index_name str: インデックス名
        expr: キー条件式

    Returns:
        list: アイテムのリスト

    Raises:
        DynamoDBError: DynamoDBのエラー
    """
    option = {"IndexName": index_name, "KeyConditionExpression": expr}
    response = table.query(**option)
    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise DynamoDBError(f"Failed to find {table.name} with {expr.get_expression()}")
    if "Items" not in response:
        raise IndexError(f"Items of {table.name} are not found with {expr.get_expression()}")
    return response["Items"]


def get_item(table, key: str, value: str) -> dict:
    """テーブルからアイテムを取得する
    Args:
        table (boto3.resource.Table): テーブル
        key (str): キー
        value (str): 値
    Returns:
        dict: アイテム
    Raises:
        DynamoDBError: DynamoDBのエラー
    """
    response = table.get_item(Key={key: value})
    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise DynamoDBError(f"Failed to find {table.name} with {key}: {value}")
    if "Item" not in response:
        raise IndexError(f"Item of {table.name} is not found with {value}")
    return response["Item"]


def post_item(table, item: dict) -> dict:
    """テーブルにアイテムを追加する
    Args:
        table (boto3.resource.Table): テーブル
        item (dict): アイテム
    Returns:
        dict: アイテム
    Raises:
        DynamoDBError: DynamoDBのエラー
    """
    response = table.put_item(Item=item, ReturnValues="NONE")
    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise DynamoDBError(f"Failed to find {table.name}")
    return item


def put_item(table, key: str, value: str, UpdExp: str, ExpAtt: dict, ExpAttName: dict = None) -> dict:
    """テーブルにアイテムを追加する
    Args:
        table (boto3.resource.Table): テーブル
        key (str): キー
        value (str): 値
        UpdExp (str): UpdateExpression
        ExpAtt (dict): ExpressionAttributeValues
    Returns:
        dict: アイテム
    Raises:
        DynamoDBError: DynamoDBのエラー
    """
    if ExpAttName is None:
        response = table.update_item(
            Key={key: value},
            UpdateExpression=UpdExp,
            ExpressionAttributeValues=ExpAtt,
            ReturnValues="ALL_NEW",
        )
    else:
        response = table.update_item(
            Key={key: value},
            UpdateExpression=UpdExp,
            ExpressionAttributeValues=ExpAtt,
            ExpressionAttributeNames=ExpAttName,
            ReturnValues="ALL_NEW",
        )
    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise DynamoDBError(f"Failed to find {table.name} with {key}: {value}")
    if "Attributes" not in response:
        raise IndexError(f"Attributes of {table.name} is not found with {value}")
    return response["Attributes"]


def delete_item(table, key: str, value: str) -> dict:
    """テーブルからアイテムを削除する
    Args:
        table (boto3.resource.Table): テーブル
        key (str): キー
        value (str): 値
    Returns:
        dict: アイテム
    Raises:
        DynamoDBError: DynamoDBのエラー
    """
    response = table.delete_item(Key={key: value}, ReturnValues="NONE")
    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise DynamoDBError(f"Failed to find {table.name} with {key}: {value}")


def delete_desk_user(desk_id: str) -> dict:
    """テーブルからデスクのユーザー情報を削除する"""
    expr = ", ".join(
        [
            "SET updated_at=:updated_at",
            "username=:username",
            "email=:email",
        ]
    )

    update_object = {
        ":updated_at": datetime.now().isoformat(),
        ":username": " ",
        ":email": " ",
    }

    try:
        response = put_item(qa_table, "desk_id", desk_id, expr, update_object)
    except DynamoDBError as e:
        raise e
    except IndexError as e:
        raise e
    return response


class DynamoDBError(Exception):
    pass
