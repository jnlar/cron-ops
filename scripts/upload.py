import bucket
import argparse
import subprocess
import os
import logging

"""
Upload a file to the S3 bucket.

Usage:
    python3 upload.py -b <bucket name> -o <object name> -f <file name>

Example:
    python3 upload.py -b my-bucket -o /path/to/object -f /path/to/file
"""
class UploadCommand:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Upload a file to the S3 bucket')
        self.parser.add_argument('--bucket', '-b', dest='bucket_name', help='The name of the S3 bucket')
        self.parser.add_argument('--object', '-o', dest='object', help='Object path')
        self.parser.add_argument('--file', '-f', dest='file', help='File path')

    def run(self):
        args = self.parser.parse_args()

        if not args.bucket_name or not args.object or not args.file:
            return self.parser.print_help()

        op = bucket.BucketOperations(args.bucket_name)

        file = os.path.basename(args.file).split('/')[-1]
        tmp = "/tmp/{}.zip".format(file)
        proc = subprocess.run(['zip', '-r', tmp , args.file], capture_output=True)

        if proc.returncode != 0:
            logging.error("Failed to compress {}".format(args.file))

            return False

        if args.file:
            op.upload(tmp, "{}/{}".format(args.object, "{}.zip".format(file)))
            proc = subprocess.run(['rm', '-f', tmp], capture_output=True)
        else:
            op.upload(args.object)

if __name__ == '__main__':
    UploadCommand().run()
