import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json


USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''

"""
Event params

{
  "access_token": "",
  "code": ""
}

or 

{
  "session": "",
  "code": ""
}

"""

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def lambda_handler(event, context):
   
    client = boto3.client('cognito-idp')
    # username = event["username"]
    # secret_hash = get_secret_hash(username)

    try:
        session=event['session']
        access_token = None
    
    except:
        access_token = event["access_token"]
    
    try:
        if not access_token:        
            resp = client.verify_software_token(
                        Session=event['session'],
                        UserCode=event['code'])
        else:
            resp = client.verify_software_token(
                        AccessToken=event['access_token'],
                        UserCode=event['code'])

    except client.exceptions.NotAuthorizedException as e:
        return {'message': "A session can be used only once", "error": True, "success": False, "data": None}
    
    except client.exceptions.CodeMismatchException as e:
        return {'message': "Wrong code entered", "error": True, "success": False, "data": None}
    
    except client.exceptions.EnableSoftwareTokenMFAException as e:
        return {'message': "VerifySoftwareToken operation Failed: Code mismatch and fail", "error": True, "success": False, "data": None}
    
    
    
    except Exception as e:
        return {'message': e.__str__(), "error": True, "success": False, "data": None}
    

    return {'message': "success", "error": False, "success": True, "data": None}