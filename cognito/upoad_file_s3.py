import json
import hashlib 
import datetime 
import boto3
import botocore

def lambda_handler(event, context):
    # TODO implement
    bucket = ""
    encrypted_filebytes = event["encrypted_filebytes"]
    file_path = event["filepath"]
    username = event["username"]
    h_username = hashlib.sha3_256(username.encode()).hexdigest()
    utc_stimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H_%M")
    
    
    
    key = f"{h_username}/{file_path}"
    
    
    tags = {"TagSet": [{"Key": "username", "Value": username},
                                {"Key": "time", "Value": utc_stimestamp}
                                ]}

    
    s3 = boto3.client('s3', region_name='ap-south-1', endpoint_url= "https://s3.ap-south-1.amazonaws.com", config=botocore.client.Config(signature_version='s3v4'))


    # upload object to amazon s3
    response = s3.put_object(Bucket=bucket, Key=key, Body=encrypted_filebytes)

    #s3.put_object_acl(Bucket=self.bucket, Key=key, ACL="public-read")
    #key.set_metadata('Content-Type', 'image/jpeg')
    s3.put_object_tagging(Bucket=bucket, Key=key, Tagging=tags)

    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return {"error": True, "success": False, "message": "file couldnt be uploaded"}
    return {"error": False, "success": True, "message": "successfully uploaded"}
    