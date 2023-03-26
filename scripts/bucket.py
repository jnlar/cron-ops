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


    def list(self):
        for object in self.bucket.objects.all():
            print(object.key)

    def delete(self, file_name):
        # FIXME
        pass
