import json
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("CO2Values")
ID = "mySensor"


def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)


def lambda_handler(event, context):
    """Sample pure Lambda function
    """
    code = 200
    body = {}
    try:
        params = event["queryStringParameters"] or {}
        begin = int(params.get("begin", "0"))
        response = table.query(
            KeyConditionExpression=Key("sensorId").eq(ID) & Key("timestamp").gte(begin)
        )
        print(response["Items"])
        body = {"items": response["Items"]}
    except KeyError:
        body["message"] = "query prameter 'begin' is required"
        code = 400
    except Exception as e:
        body["message"] = "Unexpected error is occured"
        code = 500
        print(e)

    return {
        "statusCode": code,
        "body": json.dumps(body, default=decimal_to_int),
        "headers": {"Access-Control-Allow-Origin": "*"},
    }
