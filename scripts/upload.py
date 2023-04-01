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
        self.parser.add_argument('--bucket', '-b', dest='_bucket', help='ARN for s3 bucket or bucket name')
        self.parser.add_argument('--object', '-o', dest='object', help='Object path')
        self.parser.add_argument('--file', '-f', dest='file', help='File path')

    def run(self):
        args = self.parser.parse_args()

        if not args._bucket or not args.object or not args.file:
            return self.parser.print_help()

        op = bucket.BucketOperations(args._bucket)

        if args.file[-1] == '/':
            args.file = args.file[:-1] # Remove trailing slashes 
        
        file = os.path.basename(args.file).split('/')[-1]
        tmp = "/tmp/{}.tar.bz2".format(file)
        proc = subprocess.run(['tar', '-cvjf', tmp, args.file], capture_output=True)

        if proc.returncode != 0:
            logging.error("Failed to compress {}".format(args.file))

            return False

        if args.file:
            op.upload(tmp, "{}/{}".format(args.object, "{}.tar.bz2".format(file)))
            proc = subprocess.run(['rm', '-f', tmp], capture_output=True)
        else:
            op.upload(args.object)

if __name__ == '__main__':
    UploadCommand().run()
