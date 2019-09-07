import json
import boto3
import hashlib
import hmac
import base64
# USER_POOL_ID = 'ap-south-1_56VHkSTOf'
# CLIENT_ID = '4qor0dg1sfthcv966nc22acahm'
# CLIENT_SECRET = '1dcit5nvib23g34ec5a3bun3ckcgbmt3danucvo3qn26m44bek31'

USER_POOL_ID = ''
CLIENT_ID = ''

CLIENT_SECRET = ''


PROVIDER = f'cognito-idp.ap-south-1.amazonaws.com/{USER_POOL_ID}'
client = None

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def initiate_auth(username, password):
    client = boto3.client('cognito-idp')
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
    # resp, msg = initiate_auth(event["username"], event["password"])
    # if msg != None:
    #     return {'data': None, 'message': msg, "error": True, "success": False}
        
    # result =  resp["AuthenticationResult"]
    # id_token = result["IdToken"]
    id_token = event["id_token"]
    
    identity_pool_id = "ap-south-1:3071a521-df76-464f-b677-fd8a21235ec1"
    identity_client = boto3.client('cognito-identity')

    try:
        identity_response = identity_client.get_id(IdentityPoolId=identity_pool_id, 
                                        Logins = {
    				PROVIDER: id_token
    				}
    				)
    except Exception as e:
        return {"error": True, "success": False, "message": e.__str__(), "data": None}


    identity_id = identity_response['IdentityId']
    print ('identity_id:', identity_id) # good idea not to log this

    response = identity_client.get_credentials_for_identity(
    IdentityId=identity_id,
    Logins={
        PROVIDER: id_token
       
    }
    )
    
    print (response)
    print (dir(response))
    return {'data': {
            "identity_id": identity_id,
            "access_key": response["Credentials"]["AccessKeyId"], 
            "secret_key":  response["Credentials"]["SecretKey"], 
            "session_token": response["Credentials"]["SessionToken"]}, "error": False, "success": True, "message": None}
   
