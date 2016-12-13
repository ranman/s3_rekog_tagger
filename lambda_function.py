from __future__ import print_function
import boto3
s3 = boto3.client('s3')
rekog = boto3.client('rekognition')


def lambda_handler(event, context):
    # http://docs.aws.amazon.com/lambda/latest/dg/eventsources.html#eventsources-s3-put
    try:
        for record in event['Records']:
            key = record['s3']['object']['key']
            bucket = record['s3']['bucket']['name']
            # Lambda role needs ability to access objects in bucket
            resp = rekog.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}}, MaxLabels=10)
            tags = {'TagSet': [
                {'Key': label['Name'], 'Value': str(label['Confidence'])}
                for label in resp['Labels']
            ]}
            s3.put_object_tagging(Bucket=bucket, Key=key, Tagging=tags)
    except Exception as e:
        print(e)
