import boto3
from  botocore.exceptions import *
import hmac
import hashlib
import base64
import json
def lambda_handler(event, context):
    global client
    client = boto3.client('cognito-idp')
    
    try:
        session=event["session"]
        access_token = None
    except :
        access_token=event["access_token"]
            
        
    
    try:
        if not access_token:
            response = client.associate_software_token(Session=session)
            data =  {"secret_code": response["SecretCode"], "session_token": response["Session"]}

        else:
            response = client.associate_software_token(AccessToken=access_token)
            data =  {"secret_code": response["SecretCode"], "session_token": access_token}
            
    except ParamValidationError as e:
        return {'message': resp["errorMessage"], "error": True, "success": False, "data": None}

    except client.exceptions.NotAuthorizedException:
        return {'message': "Session has expired", "error": True, "success": False, "data": None}

    except Exception as e:
        return {'message': e.__str__(), "error": True, "success": False, "data": None}

    print (response)
    return {'message': "success", "error": False, "success": True, "data": data}
    
    