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
        self.logger = logging.getLogger(__name__)

    def build_args(self):
        self.parser.add_argument('--bucket', '-b', dest='_bucket', help='ARN for s3 bucket or bucket name')
        self.parser.add_argument('--object', '-o', dest='object', help='Object path')
        self.parser.add_argument('--file', '-f', dest='file', help='File path')

        return self

    def clean(self, path):
        return path[:-1] if path[-1] == '/' else path

    def proc(self, cmd, options=None):
        # TODO: Log errors and put it somewhere
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            self.logger.error("{} {}".format(e, e.stderr.decode('utf-8')))

            return False

    def run(self):
        args = self.parser.parse_args()
        op = bucket.BucketOperations(args._bucket)
        args.file = self.clean(args.file)
        datetime = d.datetime.now().strftime('%Y%M%d-%H%M%S')

        # Only support uploading files for now
        if not args.file:
            return self.parser.print_help()

        if os.path.exists(args.file) is False:
            return self.logger.error("File or directory does not exist: {}".format(args.file))

        if os.path.isfile(args.file):
            op.upload(args.file, "{}/{}".format(self.clean(args.object), args.file))
        elif os.path.isdir(args.file):
            basename = os.path.basename(args.file)
            dirname = os.path.dirname(args.file)
            file = "{}-{}".format(basename, datetime)
            tmp = "/tmp/{}.tar.bz2".format(file)

            cmd = ['tar', '-cvjf', tmp, '-C', dirname, basename]
            self.proc(cmd)

            op.upload(tmp, "{}/{}".format(self.clean(args.object), "{}.tar.bz2".format(file)))
            self.proc(['rm', '-f', tmp])

if __name__ == '__main__':
    UploadCommand().build_args().run()
