


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



USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''




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
    # TODO implement]
    # print (dir( event['headers']))
    # print (dir(context))
    # print (dir(context.identity))
    

    dynamodb = boto3.resource('dynamodb', region_name=DYNAMODB_REGION, endpoint_url=DYNAMODB_URL)
    table = dynamodb.Table('users')
    try:
        res = delete_cognito_identity(event["username"])
        print (res)
        
        response = table.delete_item(
            Key={
                'username': event["username"],
            }
        )
        

    except Exception as e:
        return {"error": True, "success": False, "message": e.__str__(), "data": None }

    return {"error": False, "success": True, "message": "User has been deleted", "data": None }

    return 


def delete_cognito_identity(username):

    client = boto3.client('cognito-idp')
   
    try:
        response = client.admin_delete_user(
            UserPoolId=USER_POOL_ID,
            Username=username
        )
    
    
    except client.exceptions.UserNotFoundException as e:
        raise Exception("Username doesnt exists")
        
    except Exception as e:
      raise Exception(e.__str__())
    return {"error": False, "success": True, "message": f"User has been delete successfully", "data": None}
        
