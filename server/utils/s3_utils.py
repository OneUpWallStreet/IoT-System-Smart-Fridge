import boto3





# connect to the dynamoDB
s3 = boto3.resource('s3')

def get_s3_bucket(bucket_name: str):
    
    bucket = s3.Bucket(bucket_name)
    return bucket


def put_object_in_s3(bucket_name:str, key, data):
    bucket = get_s3_bucket(bucket_name)
    bucket.put_object(Key=key, Body=data)
    # return success message
    

def get_object_from_s3(bucket_name:str, key, file_name):
    bucket = get_s3_bucket(bucket_name)
    bucket.download_file(key, file_name)
    print("File downloaded")

#delete object from s3
def delete_object_from_s3(bucket_name:str, key):
    bucket = get_s3_bucket(bucket_name)
    bucket.delete_objects(Delete={'Objects': [{'Key': key}]})
    print("File deleted")

def get_presigned_url(bucket_name:str, object_name, expiration=3600):
    """Generate a presigned URL for an S3 object."""
    s3_client = boto3.client('s3', region_name='us-west-1')
    
    try:
        response = s3_client.generate_presigned_url('get_object',
            Params={'Bucket': bucket_name,
            'Key': object_name},
            ExpiresIn=expiration
            )
    except Exception as e:
        print(e)
        return None
    return response