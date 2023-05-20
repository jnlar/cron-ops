# cron-ops :tada:

AWS S3 CLI operations using [`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

> You use the AWS SDK for Python (Boto3) to create, configure, and manage AWS services, such as Amazon Elastic Compute Cloud (Amazon EC2) and Amazon Simple Storage Service (Amazon S3). The SDK provides an object-oriented API as well as low-level access to AWS services.

I use [Syncthing](https://syncthing.net/) to sync important files across devices. I don't want to deal with the send and receive only folders feature Syncthing offers[<sup>?</sup>](https://docs.syncthing.net/users/foldertypes.html#folder-types), as I want all synced devices to have write capability. So for redundancy, I use cron jobs to perform S3 operations.

### CLI

```
Usage:
    python3 upload.py -b <bucket name> -o <object name> -f <file name>
    python3 clean.py --bucket <bucket arn> --prefix <object prefix> --limit <object limit>

Example:
    0 */12 * * * /usr/bin/python3 </path/to/cron-ops>/scripts/upload.py --bucket arn:aws:s3:ap-southeast-2:111111:accesspoint/vpc-00000000000000 --file /home/user/syncthing/keepass --object dir/keepass
    0 0 * * 0 /usr/bin/python3 </path/to/cron-ops>/scripts/clean.py --bucket arn:aws:s3:ap-southeast-2:111111:accesspoint/vpc-00000000000000 --prefix dir/keepass --limit 7
```
