import logging
import boto3
from botocore.exceptions import ClientError
import os

class S3Bucket:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3')

    def get_bucket(self):
        return self.s3.Bucket(self.bucket_name)
    
class BucketOperations:
    """
    Bucket operations.

    References: 
        - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
        - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html
    """
    def __init__(self, bucket_name):
        self.bucket = S3Bucket(bucket_name).get_bucket()

    def run(self, operation, args = None):
        try:
            operation(*args)
        except ClientError as e:
            logging.error(e)
            return False

        return True

    def upload(self, file_name, object_name = None):
        if object_name is None:
            object_name = os.path.basename(file_name)

        return self.run(self.bucket.upload_file, (file_name, object_name))

    def download(self, file_name, object_name = None):
        if object_name is None:
            object_name = os.path.basename(file_name)

        return self.run(self.bucket.download_file, (object_name, file_name))

    def get_object(self, object_name):
        return self.bucket.Object(object_name).get()

    def list(self, prefix=False):
        if prefix:
            return self.bucket.objects.filter(Prefix=prefix)
        
        return self.bucket.objects.all()

    def delete(self, object):
        return self.run(self.bucket.Object(object).delete)
