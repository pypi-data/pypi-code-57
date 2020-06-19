from datetime import datetime, timedelta
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2


class TaskClient(object):

    def __init__(self, project_id, location='europe-west1'):
        self.project_id = project_id
        self.location = location
        self.client = tasks_v2.CloudTasksClient()

    def create_task(self, url, queue, payload, task_name=None, in_seconds=None):
        # Construct the fully qualified queue name.
        parent = self.client.queue_path(self.project_id, self.location, queue)

        # Construct the request body.
        task = {
            'http_request': {  # Specify the type of request.
                'http_method': 'POST',
                'url': url  # The full url path that the task will be sent to.
                }
            }
        if payload is not None:
            # The API expects a payload of type bytes.
            converted_payload = payload.encode()

            # Add the payload to the request.
            task['http_request']['body'] = converted_payload

        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            d = datetime.utcnow() + timedelta(seconds=in_seconds)

            # Create Timestamp protobuf.
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)

            # Add the timestamp to the tasks.
            task['schedule_time'] = timestamp

        if task_name is not None:
            # Add the name to tasks.
            task['name'] = task_name

        # Use the client to build and send the task.
        response = self.client.create_task(parent, task)

        print('Created task {}'.format(response.name))
        return response
