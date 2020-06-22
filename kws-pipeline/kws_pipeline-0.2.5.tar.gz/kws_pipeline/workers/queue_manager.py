from urllib.parse import urljoin

import requests


class QueueManager:
    def __init__(self, queue_manager_url, reduction_method=None):
        self.queue_manager_url = queue_manager_url
        if reduction_method:
            self.reduction = reduction_method
        else:

            def _reduce(_, __):
                pass

            self.reduction = _reduce

    def set_status(self, uuid, **kwargs):
        url = urljoin(self.queue_manager_url, str(uuid))
        r = requests.put(url, data=kwargs)
        return r

    def _reduce(self, uuid, storage_manager):
        batch_id = self.get_batch_id(uuid)
        if batch_id:
            return self.reduce_batch(batch_id, storage_manager)
        return

    def reduce_batch(self, batch_id, storage_manager):
        batch = self.get_batch(batch_id)

        if batch["progress"] < 1:
            return

        data = {
            job["uuid"]: storage_manager.read_from_file(job["uuid"])
            for job in batch["jobs_done"]
        }

        batch_result = self.reduction(data, storage_manager, batch_id)

        url = urljoin(self.queue_manager_url, f"batches/{str(batch_id)}/")
        requests.put(url, {"result_url": batch_result})
        return batch_result

    def get_batch_id(self, uuid):
        return (
            requests.get(urljoin(self.queue_manager_url, str(uuid)))
            .json()
            .get("batch_id", None)
        )

    def get_batch(self, batch_id):
        return requests.get(
            urljoin(self.queue_manager_url, f"batches/{str(batch_id)}")
        ).json()
