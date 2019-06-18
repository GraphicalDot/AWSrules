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

def initiate_auth(client, username, password):
    secret_hash = get_secret_hash(username)
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': secret_hash,
                'PASSWORD': password,
             
            },
            #these will be passed to preauthentication lambda function as it is
            ClientMetadata={
                'username': username,
                'password': password, 
                
              #  "email": email
            })
    except client.exceptions.NotAuthorizedException as e:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException as e:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    try:
        username = event['username']
    except :
        return {'message': "Please provide username to sign in", "error": True, "success": False, "data": None}
    try:
        password = event['password']
    except :
        return {'message': "Please provide password to sign in", "error": True, "success": False, "data": None}
    
    
    
    
    resp, msg = initiate_auth(client, username, password)
    if msg != None:
        return {'message': msg, "error": True, "success": False, "data": None}    
    
    
    if resp.get("AuthenticationResult"):
        return {'message': "success", "error": False, "success": True, "data": {
            "id_token": resp["AuthenticationResult"]["IdToken"], "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
            "access_token": resp["AuthenticationResult"]["AccessToken"], "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
            "token_type": resp["AuthenticationResult"]["TokenType"]
        }}
    else:
        
        return {"error": False, "success": True, "data": {"challenge_name": resp["ChallengeName"], "session_token": resp["Session"], "challenge_parameters": resp["ChallengeParameters"] }}
    