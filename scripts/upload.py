import bucket
import sys

if __name__ == '__main__':
    """
    argv, really? should probably use environment variables at some point
    """
    bucket = bucket.BucketOperations(sys.argv[1])

    if sys.argv[3]:
        bucket.upload(sys.argv[2], sys.argv[3])
    else:
        bucket.upload(sys.argv[2])
