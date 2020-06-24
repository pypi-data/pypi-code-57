from . import config
from os import path, makedirs
from google.cloud import storage
from multiprocessing.pool import ThreadPool
import logging
from datetime import datetime, timedelta
from dateutil.tz import tzutc
from google.cloud.exceptions import Forbidden


logger = logging.getLogger(__name__)


def download_data(dataset: str) -> str:
    data_root = config.AYDA_DATA_PATH
    bucket_name = config.AYDA_DATA_BUCKET

    if not bucket_name:
        logger.info("No AYDA_DATA_BUCKET specified, will not download data.")
        return dataset

    dest_path = path.join(data_root, dataset)
    makedirs(dest_path, exist_ok=True)

    client = storage.Client()
    try:
        bucket = client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=dataset)
    except Forbidden:
        logger.warning("Unable to download data. Please check your credentials")
        return dataset

    def download_blob(blob):
        if blob.name.endswith("/"):
            return
        dest_file = path.join(data_root, blob.name)
        folder_name = path.dirname(dest_file)
        makedirs(folder_name, exist_ok=True)
        do_update = not path.exists(dest_file)
        if not do_update:
            remote_time = blob.time_created - timedelta(seconds=1)
            local_time = datetime.fromtimestamp(path.getmtime(dest_file)).replace(
                tzinfo=tzutc()
            )
            if local_time < remote_time:
                do_update = True
                logger.info("File {} needs update".format(dest_file))

        if do_update:
            logger.info("Downloading {}".format(dest_file))
            for i in range(3):
                try:
                    blob.download_to_filename(dest_file)
                    break
                except Forbidden:
                    logger.warning(
                        "Could not download {}. please check your permission".format(
                            blob.name
                        )
                    )
                    return dataset
                except Exception as e:
                    logger.warning(
                        "Failed to download {}({}). Retry {}".format(blob.name, e, i)
                    )

    with ThreadPool(16) as pool:
        pool.map(download_blob, blobs)

    return dest_path
