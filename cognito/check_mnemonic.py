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
DYNAMODB_REGION = ""
TABLE_NAME = ""




def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb', region_name=DYNAMODB_REGION, endpoint_url=DYNAMODB_URL)
    table = dynamodb.Table('users')
    
    for field in ["username", "mnemonic_sha_256"]:
        if event.get(field) is None:
            return {"error": True, "success": False, "message": f"'{field}' key is required", "data": None}

    try:
        response = table.get_item(
            Key={
                'username': event["username"],
                
            }
        )
        if not response.get("Item"):
            return {"error": True, "success": False, "message": "User isn't present"}
            
        if response.get("Item")["sha_256"] != event["mnemonic_sha_256"]:
            return {"error": True, "success": False, "message": "sha3_256 hash of mnemonic didnt match", "data": None}

    except Exception as e:
        return {"error": True, "success": False, "message": e.__str__() }

    return {"error": False, "success": True, "message": "Mnemonic hash matched", "data": None}


