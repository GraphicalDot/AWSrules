import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

import decimal
DYNAMODB_URL = "http://dynamodb.ap-south-1.amazonaws.com"
DYNAMODB_REGION = "ap-south-1"
TABLE_NAME = "users"
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)



def lambda_handler(event, context):
    # TODO implement
    user_id = str(uuid.uuid4())
    dynamodb = boto3.resource('dynamodb', region_name=DYNAMODB_REGION, endpoint_url=DYNAMODB_URL)
    table = dynamodb.Table('users')
    try:
        response = table.get_item(
            Key={
                'email': event["username"],
            }
        )
        if response.get("Item"):
            return {"error": False, "success": True, "message": "User already exists"}
        else:
          response = table.put_item(
              Item={
                  'email': event["username"],
                  'user_id': user_id,
                  "created_at": decimal.Decimal(datetime.now().timestamp())
            
                }
            )
  
        
    except ClientError as e:
        return {"error": True, "success": False, "message": e.response['Error']['Message'] }

    except Exception as e:
        return {"error": True, "success": False, "message": e.__str__() }

    return {"error": False, "success": True, "message": "User successfully created"}


