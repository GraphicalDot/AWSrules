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
    dynamodb = boto3.resource('dynamodb', region_name=DYNAMODB_REGION, endpoint_url=DYNAMODB_URL)
    table = dynamodb.Table('users')
    for field in ["username", "public_key", "sha3_256", "sha3_512", "address"]:
        if event.get(field) is None:
            return  {"error": True, "success": False, "message": f"{field} is required", "data": None}
    
    if len(event["sha3_256"]) != 64:
        return  {"error": True, "success": False, "message": f"Invalid length of sha256 hash of mnemonic", "data": None}
        
    if len(event["sha3_512"]) != 128:
        return  {"error": True, "success": False, "message": f"Invalid length of sha512 hash of mnemonic", "data": None}
    
    if len(event["public_key"]) != 66:
        return  {"error": True, "success": False, "message": f"Invalid length of public_key, must be ", "data": None}
    
    
    if len(event["address"]) != 34:
        return  {"error": True, "success": False, "message": f"Invalid length of address, must be 34", "data": None}
    
    username = event["username"]    
    try:
        response = table.update_item(
                Key={"username": event['username']},
                
                UpdateExpression='SET public_key=:public_key, sha3_256=:sha3_256, sha3_512=:sha3_512, address=:address',
                ConditionExpression="username = :u",
                ExpressionAttributeValues={
                        ':u': username,
                        ':public_key': event["public_key"],
                        ':sha3_256': event["sha3_256"],
                        ':sha3_512': event["sha3_512"],
                        ':address': event["address"]
                    },
              
            )
        print (response)


    except Exception as e:
        print (e)
        return {"error": True, "success": False, "message": "Username doesnt exists", "data": None}

    return {"error": False, "success": True, "message": "Entry successfully updated", "data": None}


