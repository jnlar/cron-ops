import argparse
import bucket
from datetime import datetime, timedelta
import logging

"""
Clean up old files from the S3 bucket
"""
class CleanCommand:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Upload a file to the S3 bucket')
        self.logger = logging.getLogger(__name__)

    def build_args(self):
        self.parser.add_argument('--bucket', '-b', dest='_bucket', help='ARN for s3 bucket or bucket name')
        self.parser.add_argument('--prefix', '-p', dest='prefix', help='Prefix path')
        self.parser.add_argument('--limit', '-l', dest='limit', help='Limit timeframe')

        return self

    def run(self):
        args = self.parser.parse_args()
        op = bucket.BucketOperations(args._bucket)

        files = op.list(args.prefix)

        for file in files:
            object = op.get_object(file.key)

            last_modified = object['LastModified']
            limit = datetime.now() - timedelta(days=args.limit)

            # Use timestamps to avoid offset naive vs offset aware issues. 
            if last_modified.timestamp() < limit.timestamp():
                op.delete(file.key)

if __name__ == '__main__':
    CleanCommand().build_args().run()