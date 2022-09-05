import os
import io
import boto3
from botocore.exceptions import ClientError
from typing import Union, Optional, Tuple
from logger_utils import logger


class S3Service:
    """S3 service class to provide for S3 utilities"""

    def __init__(self, ):
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        self.client = boto3.client("s3", aws_access_key_id=self.aws_access_key,
                                   aws_secret_access_key=self.aws_secret_key)

    def send_to_s3(self, content: io.BytesIO, bucket: str, object_name: str = None) -> Tuple[bool, Optional[str]]:
        """Upload a file to an S3 bucket.
           :param file_name: File to upload.
           :param bucket: Bucket to upload.
           :param object_name: S3 object name. If not specified then file_name is used.
           :return: True, None if file was uploaded, False, error message if not.
        """

        config_pass = (self.aws_access_key is not None and
                       self.aws_secret_key is not None )
        if not config_pass:
            return False, "S3 Configuration Error: S3 Upload Failed"

        # If S3 object_name was not specified, use the file name.

        try:
            self.client.upload_fileobj(content, bucket, object_name)
        except ClientError as e:
            return False, e.response
        return True, None

    def get_from_s3_utf8(self, id: str, bucket: str) -> Tuple[Optional[dict], Optional[str]]:

        fbytes, error = self.get_from_s3(id, bucket)
        if error is not None:
            return None, error
        return {"file": fbytes.decode("utf-8")}, None

    def get_from_s3(self, id: str, bucket: str) -> Tuple[Optional[bytes], Optional[str]]:

        config_pass = (self.aws_access_key is not None and
                       self.aws_secret_key is not None)
        if not config_pass:
            return None, "S3 Configuration Error: S3 Upload Failed"
        try:
            with io.BytesIO() as f:
                self.client.download_fileobj(bucket, id, f)
                f.seek(0)
                return f.read(), None
        except ClientError as e:
            return None, e.response



    def list_bucket(self, bucket: str, prefix: str = None) -> Tuple[Union[dict, bool], Optional[str]]:
        """
        Lists the objects in a bucket, optionally filtered by a prefix.

        :param bucket: The bucket to query.
        :param prefix: When specified, only objects that start with this prefix are listed.
        :return: The list of objects.
        """
        try:
            if not prefix:
                objects = self.client.list_objects_v2(Bucket=bucket)
            else:
                objects = self.client.list_objects_v2(Bucket=bucket, Prefix=prefix)
            logger.info("Got objects %s from bucket '%s'",
                        [o["Key"] for o in objects["Contents"]], bucket)
        except ClientError as e:
            logger.exception("Couldn't get objects for bucket '%s'.", bucket)
            return False, e.response
        else:
            return objects, None

