
# This file is used to test the S3 bucket named "foodpicutes". It grabs the list of items in the bucket and prints them out. 
# It also uploads a file called "brain.png"  to the bucket and then prints out the list of items in the bucket again.
# Last it downloads the file "jack.png" from the bucket and saves it as "jack.png" in the current directory.

import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# connect to the S3 bucket
#hello 
s3 = boto3.resource('s3')

# get the bucket named "foodpicutes"

bucket = s3.Bucket('foodpicutes')

# print items in the bucket

for obj in bucket.objects.all():
    print(obj.key)

# upload a file to the bucket

data = open('brain.png', 'rb')

bucket.put_object(Key='brain.png', Body=data)

# print items in the bucket

for obj in bucket.objects.all():

    print(obj.key)

# download a file from the bucket

bucket.download_file('jack.png', 'jack.png')

print("File downloaded")
