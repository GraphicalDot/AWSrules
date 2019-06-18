import json
import hashlib
import datetime
import boto3
import botocore
BUCKET_NAME = "datapod-backups"
def lambda_handler(event, context):

    s3 = boto3.client('s3', region_name='ap-south-1', endpoint_url= "https://s3.ap-south-1.amazonaws.com", config=botocore.client.Config(signature_version='s3v4'))

    username = event["username"]
    key = hashlib.sha3_256(username.encode()).hexdigest()
    utc_stimestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H_%M")
    print (utc_stimestamp)
    params = {
        'Bucket': BUCKET_NAME,
        'Key': f"{key}/{utc_stimestamp}",
    }
    url = s3.generate_presigned_url('put_object', Params=params, ExpiresIn=72000, HttpMethod='PUT')
    #    url = s3.generate_presigned_post(Bucket=BUCKET_NAME, Key= f"{key}/{utc_stimestamp}")
    return {"url": url}