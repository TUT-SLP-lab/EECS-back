import os

import boto3
from boto3.dynamodb.conditions import Key

PR_NUM = os.environ["PR_NUM"]

# TODO: TABLE名を用意する。
# LIKE: QA_TABLE = f"qa-{PR_NUM}"

dynamodb = boto3.resource("dynamodb")
# TODO: TABLEを用意する。
# LIKE: qa_table = dynamodb.Table(QA_TABLE)


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


# TODO: POST, PUT, DELETEの実装


class DynamoDBError(Exception):
    pass
