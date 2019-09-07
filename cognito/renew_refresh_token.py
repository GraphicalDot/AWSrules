
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json




USER_POOL_ID = ''
CLIENT_ID = ''
CLIENT_SECRET = ''

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

def initiate_auth(client, refresh_token, username):
    secret_hash = get_secret_hash(username)
    try:
        resp = client.initiate_auth(
            #UserPoolId=USER_POOL_ID,
            
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': secret_hash,
                'REFRESH_TOKEN': refresh_token,
             
            },
            ClientId=CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            )
    except client.exceptions.NotAuthorizedException as e:
        print (e)
        return None, "Invalid refresh token or username is incorrect or Refresh Token has been revoked"
        
    except client.exceptions.UserNotConfirmedException as e:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None

def lambda_handler(event, context):
    
    for field in ["username", "refresh_token"]:
        if event.get(field) is None:
            return {'message': f"Please provide {field} to renew tokens", "error": True, "success": False, "data": None}
    client = boto3.client('cognito-idp')
    
    
    
    resp, msg = initiate_auth(client, event["refresh_token"], event["username"])
    print (resp)
    if msg != None:
        return {'message': msg, "error": True, "success": False, "data": None}    
    
    # response = client.admin_user_global_sign_out(
    #         UserPoolId=USER_POOL_ID,
    #         Username=event["username"]
    #     )
    if resp.get("AuthenticationResult"):
        return {'message': "success", "error": False, "success": True, "data": {
            "id_token": resp["AuthenticationResult"]["IdToken"],
            "access_token": resp["AuthenticationResult"]["AccessToken"], "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
            "token_type": resp["AuthenticationResult"]["TokenType"]
        }}
    else:
        return {'message': "Refresh token couldnt refreshed", "error": True, "success": False, "data": None}    

        
    