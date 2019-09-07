import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json




USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''



def lambda_handler(event, context):
    
    for field in ["username"]:
        if event.get(field) is None:
            return {'message': f"Please provide {field} to renew tokens", "error": True, "success": False, "data": None}
    client = boto3.client('cognito-idp')
    
    
    try:
        client.admin_user_global_sign_out(
                UserPoolId=USER_POOL_ID,
                Username=event["username"]
            )
            
    except Exception as e:
        return {'message': e.__str__(), "error": True, "success": False, "data": None}
    
    return {'message': "User successfully logged out", "error": False, "success": True, "data": None}
    
    
    