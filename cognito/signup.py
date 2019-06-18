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
    
def sign_up(username, password,  name, email):
    
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password, 
            UserAttributes=[
            {
                'Name': "name",
                'Value': name
            },
            {
                'Name': "email",
                'Value': email
            }
            ],
            ValidationData=[
                {
                'Name': "email",
                'Value': email
            },
            {
                'Name': "custom:username",
                'Value': username
            }

            ],
      
            )
        print(resp)
    except client.exceptions.UsernameExistsException as e:
        return USER_EXISTS, e.__str__()

    except Exception as e:
        return ERROR, e.__str__()
    print ("error")
    return SUCCESS, None



def lambda_handler(event, context):
    print (event)
    global client
    if client == None:
        client = boto3.client('cognito-idp')

    username = event['username']
    email = event["email"]
    password = event['password']
    name = event["name"]

    #email = event['email']
    is_new = False
    signed_up, msg = sign_up(username, password, name, email)
    if msg != None:
        return {'msg': msg, "error": True, "success": False}
    
    return {"error": False, "success": True, 'msg': "Please confirm your signup, check Email for validation code"}
    