import argparse
import bucket
import datetime as d
import logging
import os
import subprocess

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
        self.logger = logging.getLogger(__name__)

    def clean(self, path):
        return path[:-1] if path[-1] == '/' else path

    def proc(self, cmd, options=None):
        # TODO: Log errors and put it somewhere
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            self.logger.error("{} {}".format(e, e.stderr.decode('utf-8')))

            return False

    def run(self):
        args = self.parser.parse_args()
        op = bucket.BucketOperations(args._bucket)
        
        file = "{}-{}".format(d.date.today(), os.path.basename(self.clean(args.file)).split('/')[-1])
        tmp = "/tmp/{}.tar.bz2".format(file)
        self.proc(['tar', '-cvjf', tmp, args.file]):

        # Only file upload support for now
        if args.file:
            op.upload(tmp, "{}/{}".format(self.clean(args.object), "{}.tar.bz2".format(file)))
            self.proc(['rm', '-f', tmp])
        else:
            return self.parser.print_help()

if __name__ == '__main__':
    UploadCommand().run()
