import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid



USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''

"""
event args
{
  "enabled": true,
  "access_token": ""
}

"""


def lambda_handler(event, context):
    try:
        access_token = event["access_token"]
    except:
        return {"error": True, "success": False, "message": "Please provide access_token", "data": None}


    
    client = boto3.client('cognito-idp')    
    try:
        print (access_token)
        response = client.set_user_mfa_preference(
            SoftwareTokenMfaSettings={
                'Enabled': event["enabled"],
            
            },
            AccessToken=access_token

        )
    
    except client.exceptions.NotAuthorizedException as e:
        return {"error": True, "success": False, "message": "Invalid Access Token", "data": None}

    except Exception as e:
        return {"error": True, "success": False, "message": e.__str__(), "data": None}
    
    return {"error": True, "success": False, "message": None, "data": None}