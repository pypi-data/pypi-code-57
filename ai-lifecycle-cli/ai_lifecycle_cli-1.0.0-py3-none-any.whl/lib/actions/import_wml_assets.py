#  © Copyright IBM Corporation 2020.

import time
import datetime

from ai_lifecycle_cli.lib.utils.LoggingHandler import LoggingHandler


logger = LoggingHandler()


def execute(client, container_id, container_type, archive_file, timeout):
    """
    Perform import task on CP4D cluster in version 3.0 or higher
    :param client:
    :param space_id:
    :param archive_file:
    :param timeout:
    :return: space ID and status of import task
    """
    space_id = container_id
    import_path = "/v4/spaces/{}/imports".format(space_id)
    import_path_with_id = ""

    with open(str(archive_file), 'rb') as archive:
        data = archive.read()
        space_import_res = client.make_request('post', path=import_path, data=data)

        if not space_import_res.ok:
            raise Exception("Failed to initialize import, %s" % space_import_res.content)

        import_path_with_id = space_import_res.headers['Location']
        import_id = str(import_path_with_id).split('/')[-1]
        logger.log_info(
            "Initialized import task with ID {task_id} in space with ID {space_id}".format(task_id=import_id,
                                                                                           space_id=space_id))

    start = datetime.datetime.now()
    elapsed = datetime.datetime.now() - start

    import_status = ""
    while True and elapsed.total_seconds() < timeout:
        import_task_res = client.make_request('get', path=import_path_with_id)
        if not import_task_res.ok:
            raise Exception("Failed to get import status, %s" % import_task_res.content)
        import_status = import_task_res.json()['entity']['status']['state']
        logger.log_info(
            "Import {import_id} status: {status}".format(import_id=import_id,
                                                         status=import_status)
        )

        if import_status == "completed":
            logger.log_info(
                "Import status: {state} - progress: {progress}%".format(state=import_status, progress=100))
            logger.log_info(
                "Finished import task with ID {import_id} to space ID {space_id}".format(import_id=import_id,
                                                                                         space_id=space_id))
            break
        if import_status == "failed":
            cancel_import_task_res = client.make_request('delete', path=import_path_with_id)
            if not cancel_import_task_res.ok:
                raise Exception("Failed to import and to cancel import job, %s" % cancel_import_task_res.content)
            raise Exception("Failed to import, %s" % import_task_res.content)
        import_progress = int(import_task_res.json()['entity']['status'].get('progress', 0)) * 100
        logger.log_info(
            "Import status: {state} - progress: {progress}%".format(state=import_status, progress=import_progress))
        elapsed = datetime.datetime.now() - start
        if elapsed.total_seconds() > timeout:
            cancel_import_task_res = client.make_request('delete', path=import_path_with_id)
            if not cancel_import_task_res.ok:
                raise Exception("Failed to cancel import job, %s" % cancel_import_task_res.content)
            logger.log_warning(
                "Cancelled import {import_id} due to timeout of {duration} seconds.".format(import_id=import_id, duration=timeout))
            return space_id, "canceled"
        time.sleep(3)

    return space_id, import_status
