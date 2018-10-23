import boto3

s3 = boto3.client('s3')

#create s3 bucket
try:
    response = s3.create_bucket(
                Bucket= 'haha'
    )
except s3.exceptions.BucketAlreadyExists as e:
    print("bucket already exists!")






