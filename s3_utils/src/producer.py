import os
from logger_utils import logger
import argparse
from utils.general import generate_id_by_timestamp
from aws_utils.s3_service import S3Service


class Producer:
    def __init__(self):
        self.s3_cleint = S3Service()

    def run(self):
        # get object list in sample Bucket
        bucket_obj, error = self.s3_cleint.list_bucket(os.getenv("AWS_SAMPLE_BUCKET"))
        if error is not None:
            return False, error

        # for each object bucket_obj["Contents"]
        # Download from source bucket
        # upload to consumer Bucket
        # delete bucket
        return True, None


def run() -> bool:

    app_status, error = Producer().run()
    if error is not None:
        logger.error(error)
    return True


if __name__ == "__main__":

    cron_id = generate_id_by_timestamp()
    cmd_config = {
        "CRONID": cron_id,
        "EMAIL_ENABLED": True,
    }
    parser = argparse.ArgumentParser(description="Producer for Web Service based Transactions")
    parser.add_argument("--no_email", help="Don't Send Emails", action="store_true")
    args = parser.parse_args()

    if args.no_email:
        cmd_config["EMAIL_ENABLED"] = False

    run()
