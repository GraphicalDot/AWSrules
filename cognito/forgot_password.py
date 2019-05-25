
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

client = None
def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

def lambda_handler(event, context):
    global client
    if client == None:
        client = boto3.client('cognito-idp')

    
    
    try:
        username = event['username']

        response = client.forgot_password(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            UserContextData={
                'EncodedData': 'string'
            },
            AnalyticsMetadata={
                'AnalyticsEndpointId': 'string'
            }
        )

    except client.exceptions.UserNotFoundException as e:
        return {"error": True, "success": False, "message": "Username doesnt exists"}
        
    except client.exceptions.InvalidParameterException as e:
        return {"error": True, "success": False, "message": f"User <{username}> is not confirmed yet"}
    
    except client.exceptions.CodeMismatchException as e:
        return {"error": True, "success": False, "message": "Invalid Verification code"}
        
    except client.exceptions.NotAuthorizedException as e:
        return {"error": True, "success": False, "message": "User is already confirmed"}
    
    except Exception as e:
        return {"error": True, "success": False, "message": f"Uknown error {e.__str__()} "}
     
    print ("This is the response",  response) 
    return event

