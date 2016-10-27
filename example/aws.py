#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import configparser
from pathlib import Path
from boto3.session import Session
from boto3.s3.transfer import S3Transfer
from boto3.s3.transfer import TransferConfig

# ref: http://www.pyfunctional.org/
# pip install pyfunctional
from functional import seq

# ref: http://awesome-python.com/
# ref: http://docs.python-cerberus.org/
# ref: https://docs.python.org/3/library/re.html
# ref: http://pythex.org/
import re


# =============================================
# Defines
# =============================================
NOW = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
CREDENTIAL_FPATH = os.path.join(SCRIPT_DIR, 's3_credentials')


# =============================================
# Func
# =============================================
def gen_s3_paths(client, bucket, prefix):
    paginator = client.get_paginator('list_objects')
    page_iterator = paginator.paginate(
        Bucket=bucket,
        Prefix=prefix,
        Delimiter='/'
    )
    try:
        for result in page_iterator:
            for prefix in result['Contents']:
                yield prefix.get('Key')
    except:
        return

def get_paths(dir_path, glob_str='**/*'):
    paths = Path(dir_path).glob(glob_str)
    return (seq(paths)
            .map(lambda x: Path(x))
            .filter(lambda x: x.is_file())
            .map(lambda x: x.as_posix()))

class S3Manager:
    def __init__(self, config_fpath):
        credentials = configparser.ConfigParser()
        credentials.read(config_fpath)
        aws_access_key_id = credentials.get('default', 'aws_access_key_id')
        aws_secret_access_key = credentials.get('default', 'aws_secret_access_key')
        session = Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='ap-northeast-1'
        )

        config = TransferConfig(
            # multipart_threshold=8 * 1024 * 1024,
            max_concurrency=10,
            num_download_attempts=10,
        )

        self.s3 = session.resource('s3')
        self.client = session.client('s3')
        self.transfer = S3Transfer(self.client, config)

    def filelist_s3(self, bucket_name, prefix):
        return list(gen_s3_paths(self.client, bucket_name, prefix))

    def download_s3(self, bucket_name, prefix, download_dir):
        # validate prefix name
        # validate download_dir name
        os.makedirs(os.path.join(download_dir, prefix), exist_ok=True)
        s3_paths = list(gen_s3_paths(self.client, bucket_name, prefix))

        for s3_path in s3_paths:
            if s3_path == prefix:
                continue
            filename = os.path.join(download_dir, s3_path)
            self.transfer.download_file(
                bucket=bucket_name,
                key=s3_path,
                filename=filename
            )
            # print('[download] {0}:{1} => {2}'.format(bucket_name, s3_path, filename))

    def upload_s3(self, bucket_name, prefix, upload_paths):
        for path in upload_paths:
            basename = os.path.basename(path)
            key = Path(prefix, basename).as_posix()
            self.transfer.upload_file(
                filename=path,
                bucket=bucket_name,
                key=key,
                extra_args={'ACL': 'public-read'}
            )
            # print('[upload]{0} => {1}:{2}'.format(path, bucket_name, key))


if __name__ == "__main__":
    upload_paths = []


    s3_manager = S3Manager(CREDENTIAL_FPATH)
    s3_files = s3_manager.filelist_s3(BUCKET_NAME, prefix)

    ## check file exist
    if s3_files:
        s3_manager.download_s3(bucket_name, prefix, backup_dir)

    ## upload s3
    s3_manager.upload_s3(bucket_name, prefix, upload_paths)

    ## check uploaded file
    s3_files = s3_manager.filelist_s3(BUCKET_NAME, prefix)
    print('[DONE] {0}'.format(s3_files))
