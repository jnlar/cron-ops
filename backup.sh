#!/bin/bash

# FIXME: lets log stuff
syncthing_dir='/home/ubuntu/syncthing'
dest='s3://crunchy-freezable-moaner-gating/ec2-syncthing/'
date=$(date +"%Y-%m-%d")
backup="syncthing-$(echo $date).zip"

zip -r /tmp/$(echo $backup) $syncthing_dir > /dev/null 2>&1
/usr/bin/aws s3 cp /tmp/$(echo $backup) $dest > /dev/null 2>&1
rm -f /tmp/$(echo $backup)
