import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json



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

ERROR = 0
SUCCESS = 1
USER_EXISTS = 2
    
def sign_up(username, password):

    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password, 
  
            )
        print(resp)
    except client.exceptions.UsernameExistsException as e:
        return USER_EXISTS

    except Exception as e:
        print(e)
        return ERROR
    print ("error")
    return SUCCESS

    
def initiate_auth(username, password):
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': get_secret_hash(username),
                'PASSWORD': password,
             
            },
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
    global client
    if client == None:
        client = boto3.client('cognito-idp')

    username = event['username']
    password = event['password']
    #email = event['email']
    is_new = False
    signed_up = sign_up(username, password)
    if signed_up == ERROR:
        print ('failed to sign up')
        return {'status': 'fail', 'msg': 'failed to sign up'}
    if signed_up == SUCCESS:
        print ('Success in  sign up')

        is_new = True
    
    resp, msg = initiate_auth(username, password)
    if msg != None:
        return {'status': 'fail', 'msg': msg, "error": True, "success": False, "is_new": is_new}
    id_token = resp['AuthenticationResult']['IdToken']

    return {"error": False, "success": True, 'id_token': id_token, 
        'is_new': is_new}
        
def get_user(token):
    response = client.get_user(
    AccessToken=token
    )
    return response