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
    def __init__(self, bucket_name):
        self.bucket = S3Bucket(bucket_name).get_bucket()

    def upload(self, file_name, object_name = None):
        """
        Upload a file to the S3 bucket

        Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
        """
        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            self.bucket.upload_file(file_name, object_name)
        except ClientError as e:
            logging.error(e)
            return False

        return True

    def download(self, file_name):
        self.bucket.download_file(file_name, file_name)

    def list(self):
        return self.bucket.objects.all()

    def delete(self, file_name):
        self.bucket.Object(file_name).delete()
