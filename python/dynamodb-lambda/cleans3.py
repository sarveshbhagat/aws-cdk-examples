import os
import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Call S3 to list current buckets
response = s3.list_buckets()

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]

bukcet_list = []

for bucket in buckets:
    if (bucket.startswith('consumer')):
        bukcet_list.append(bucket)
    if (bucket.startswith('producer')):
        bukcet_list.append(bucket)

for each in bukcet_list:
    cmd = "aws s3 rm s3://" + each + " --recursive"
    print(cmd)
    os.system(cmd)

# aws s3api delete-bucket --bucket

for each in bukcet_list:
    cmd = "aws s3api delete-bucket --bucket " + each
    try:
        os.system(cmd)
    except:
        pass
