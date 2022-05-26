# Program to convert Json Files to yaml and transfer it to appropriate S3 buckets
import json
import os.path
import time
import urllib.request
import urllib.response
import urllib.error
import boto3
print('Function start (CloudWatch)')

s3 = boto3.client('s3')


def lamda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    copy_source = {'Bucket': source_bucket, 'Key': key}

    # CloudWatch Info
    print("Lod Stream Name: ", context.log_stream_name)
    print("Log Group Name: ", context.log_group_name)
    print("Request ID: ", context.aws_request_id)
    print("Start of try")

    # Logic
    try:
        writer = s3.get_waiter('object_exists')
        writer.wait(Bucket=source_bucket, Key=key)

        # Get the file extension
        extension = os.path.splitext(key)[1]

        # Copy from S3 to S3
        if extension == ".yaml":
            s3.copy_object(Bucket='files-yaml-bucket',
                           Key=key, CopySource=copy_source)
        if extension == ".json":
            s3.copy_object(Bucket='files-json-bucket',
                           Key=key, CopySource=copy_source)

    except Exception as e:
        print(e)
        print("Error while copying the files. Does not exists".format(key,source_bucket))
        raise e

    print("End of function")