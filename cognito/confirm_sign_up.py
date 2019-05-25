import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid

import decimal


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
    print ("Execution started")
    global client
    if client == None:
        client = boto3.client('cognito-idp')

    
    try:
        
        username = event['username']
        code = event['code']

        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            ConfirmationCode=code,
            ForceAliasCreation=False,
            # AnalyticsMetadata={
            #     'AnalyticsEndpointId': 'string'
            # },
            # UserContextData={
            #     'EncodedData': 'string'
            # }
             )
        print (response)

    except client.exceptions.UserNotFoundException as e:
        return {"error": True, "success": False, "message": "Username doesnt exists"}
        
    except client.exceptions.CodeMismatchException as e:
        return {"error": True, "success": False, "message": "Invalid Verification code"}
        
    except client.exceptions.NotAuthorizedException as e:
        return {"error": True, "success": False, "message": "User is already confirmed"}
    
    except client.exceptions.LimitExceededException as e:
        return {"error": True, "success": False, "message": "Attempt limit exceeded, please try after some time"}
    
    except Exception as e:
        return {"error": True, "success": False, "message": f"Uknown error {e.__str__()} "}

    lambda_client = boto3.client('lambda')
    invoke_response = lambda_client.invoke(FunctionName="dynamo_db_put",
                                           InvocationType='Event',
                                           Payload=json.dumps(event))
    print(invoke_response)
    return {"error": True, "success": False, "message": f"The user has been confirmed, Please sign in"}

