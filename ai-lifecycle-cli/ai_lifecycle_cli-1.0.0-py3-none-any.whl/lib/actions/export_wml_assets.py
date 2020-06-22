#  © Copyright IBM Corporation 2020.

import time
import datetime

from pathlib import Path
from ai_lifecycle_cli.lib.clients.rest_client import RESTClient
from ai_lifecycle_cli.lib.utils.FsHandler import FsHandler
from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler


logger = LoggingHandler()


def execute(client, sources, timeout):
    """
    Perform export task on CP4D cluster in version 3.0 or higher
    :param client:
    :param sources:
    :param timeout:
    :return: space ID and status of export task
    """
    export_path = "/v4/spaces/{}/exports"
    export_path_with_id = ""

    export_items = []

    space_sources = sources.get("space")
    if space_sources is not None:
        for space in space_sources:
            space_id = space['guid']
            space_export_path = export_path.format(space_id)
            export_body = dict(
                name="Export job for space {}".format(space_id),
                assets=space['assets']
            )
            space_export_res = client.make_request('post', path=space_export_path, body=export_body)

            if not space_export_res.ok:
                raise Exception("Failed to initialize export, %s" % space_export_res.content)

            export_path_with_id = space_export_res.headers['Location']

            start = datetime.datetime.now()
            elapsed = datetime.datetime.now() - start

            export_status = ""
            while True and elapsed.total_seconds() < timeout:
                export_task_res = client.make_request('get', path=export_path_with_id)
                if not export_task_res.ok:
                    raise Exception("Failed to get export status, %s" % export_task_res.content)
                export_status = export_task_res.json()['entity']['status']['state']

                export_id = str(export_path_with_id).split('/')[-1]
                if export_status == "completed":
                    logger.log_info(
                        "Export status: {state} - progress: {progress}%".format(state=export_status, progress=100))
                    logger.log_info(
                        "Finished export task with ID {export_id} from space ID {space_id}".format(export_id=export_id,
                                                                                                 space_id=space_id))
                    break
                if export_status == "failed":
                    cancel_export_task_res = client.make_request('delete', path=export_path_with_id)
                    if not cancel_export_task_res.ok:
                        raise Exception("Failed to export and to cancel export job, %s" % cancel_export_task_res.content)
                    raise Exception("Failed to export, %s" % export_task_res.content)
                export_progress = int(export_task_res.json()['entity']['status'].get('progress', 0)) * 100
                logger.log_info(
                    "Export status: {state} - progress: {progress}%".format(state=export_status, progress=export_progress))
                elapsed = datetime.datetime.now() - start
                if elapsed.total_seconds() > timeout:
                    cancel_export_task_res = client.make_request('delete', path=export_path_with_id)
                    if not cancel_export_task_res.ok:
                        raise Exception("Failed to cancel export job, %s" % cancel_export_task_res.content)
                    logger.log_warning(
                        "Cancelled export {export_id} due to timeout of {duration} seconds.".format(export_id=export_id,
                                                                                                        duration=timeout))
                    return list(), list()
                time.sleep(3)

            export_id = export_path_with_id.split('/')[-1]
            export_items.append((space_id, export_id))

    files = download_content(client, export_items)

    return list(), files


def download_content(client, exports):
    """
    Download content from successfully exported spaces
    :param client:
    :param exports:
    :return:
    """

    fs = FsHandler()
    fs.setup_default_dir()

    export_content_path = "/v4/spaces/{}/exports/{}/content"

    space_ids = []
    content_statuses = []
    archived_files = []


    for export_item in exports:
        space_export_content_path = export_content_path.format(export_item[0], export_item[1])
        space_export_content_res = client.make_request('get', path=space_export_content_path)

        if not space_export_content_res.ok:
            raise Exception("Failed to download exported content, %s" % space_export_content_res.content)

        archive_path = Path(str(fs.get_default_dir()) + "/{}_{}.zip".format(export_item[0], fs.ts_now))
        with open(str(archive_path), 'wb') as archive:
            archive.write(space_export_content_res.content)
            archived_files.append(str(archive_path))

    return archived_files
