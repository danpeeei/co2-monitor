import json
import os
import time

import boto3
import requests

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("CO2Values")
ID = "mySensor"
TTL = 60 * 60 * 24  # 24 hour
TOKEN = os.environ["TOKEN"]
URL = "https://notify-api.line.me/api/notify"


def send_line_notify(message: str):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"message": message}
    response = requests.post(URL, headers=headers, data=data)
    response.raise_for_status()


def lambda_handler(event, context):
    """Sample pure Lambda function
    """
    now = int(time.time())
    code = 200
    message = "OK"
    try:
        co2 = int(event["queryStringParameters"]["co2"])
        _ = table.put_item(
            Item={"sensorId": ID, "co2": co2, "timestamp": now, "ttl": now + TTL}
        )
        print(_)
        if co2 >= 1000:
            send_line_notify(f"換気しませんか？CO2濃度は {co2}ppmです")
    except KeyError:
        code = 400
        message = "co2 is not specified"
    except Exception as e:
        message = "Unexpected error is occured"
        print(e)

    return {
        "statusCode": code,
        "body": json.dumps({"message": message}),
    }
