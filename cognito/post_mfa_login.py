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

def lambda_handler(event, context):
   
    client = boto3.client('cognito-idp')
    username = event["username"]
    secret_hash = get_secret_hash(username)

    try:
        resp = client.admin_respond_to_auth_challenge(
             UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            ChallengeName='SOFTWARE_TOKEN_MFA',
            Session=event['session'],
            ChallengeResponses={
             'USERNAME': username,
            'SECRET_HASH': secret_hash,
            "SOFTWARE_TOKEN_MFA_CODE": event["mfa_code"]
            })
        

    except client.exceptions.NotAuthorizedException as e:
        return {'message': "A session can be used only once", "error": True, "success": False, "data": None}
    
    except client.exceptions.CodeMismatchException as e:
        return {'message': "Wrong code entered", "error": True, "success": False, "data": None}
    
    except Exception as e:
        return {'message': e.__str__(), "error": True, "success": False, "data": None}

    return {'message': "success", "error": False, "success": True, "data": {
            "id_token": resp["AuthenticationResult"]["IdToken"], "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
            "access_token": resp["AuthenticationResult"]["AccessToken"], "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
            "token_type": resp["AuthenticationResult"]["TokenType"]
    }}