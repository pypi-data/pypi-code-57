"""Provides PrepareTask class."""
import copy
import logging

import fs

from .. import schemas as T
from .. import utils
from .abstract import Task

log = logging.getLogger(__name__)


class PrepareTask(Task):
    """Preprocessing work."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_containers = self.db.batch_writer_update_container()
        self.update_items = self.db.batch_writer_update_item(depends_on=self.update_containers)
        self.insert_tasks = self.db.batch_writer_insert_task(depends_on=self.update_items)
        # keep cache size in sync with the size of the update containers batch writer
        # this simplify how we find the already created containers
        # otherwise we should check the batch writer buffer and
        # if the container is not there query the db
        # How can cache miss happen?
        # postgres sorts strings using LC_COLLATE and it can produce different results
        # hu_HU.utf8: ['sub_1', 'sub_1/sub_sub', 'sub_10']
        # en_US.utf8: ['sub_1', 'sub_10', 'sub_1/sub_sub']
        self.cache = utils.LRUCache(self.update_containers.batch_size)
        self.valid_container_paths = set()
        self.valid_item_ids = set()

    def _run(self):
        """Process review, create and enqueue upload tasks"""
        self.report_progress(total=self.db.count_all_container())
        for item in self.db.get_items_with_error_count():
            if item.container_error or self._should_skip_item(item):
                self.update_items.push({"id": item.id, "skipped": True})
                continue
            self.valid_container_paths.add(item.container_path)
            self.valid_item_ids.add(item.id)

        # create new containers
        for container in self.db.get_all_container():
            # check if the container path is in the valid containers
            valid = False
            for path in self.valid_container_paths:
                if path.startswith(container.path):
                    valid = True
                    break

            # always create project and group containers
            if not valid and container.level.name != "project" and container.level.name != "group":
                # update progress
                self.report_progress(completed=1)
                continue

            # get parents here to keep cache warm
            ancestors = self._get_parents(container)
            if not container.dst_context:
                self._create_container(container, ancestors)
            # cache the container
            self.cache[container.id] = container

            # update progress
            self.report_progress(completed=1)

        self.report_progress(force=True)

        self.db.set_ingest_status(status=T.IngestStatus.uploading)

        for item_id in self.valid_item_ids:
            self.insert_tasks.push(T.TaskIn(
                type=T.TaskType.upload,
                item_id=item_id,
            ).dict())

        # this flush implicitly calls update_containers.flush()
        # and update_items.flush() because of dependency
        self.insert_tasks.flush()

    def _create_container(self, container, ancestors):
        c_level = container.level.name
        create_fn = getattr(self.fw, f"add_{c_level}", None)
        parent = ancestors.get(container.parent_id)
        if not create_fn:
            raise ValueError(f"Unsupported container type: {c_level}")
        create_doc = copy.deepcopy(container.src_context)
        if c_level == "session":
            # Add subject to session
            project = ancestors[parent.parent_id]
            create_doc["project"] = project.dst_context["_id"]
            create_doc["subject"] = {"_id": parent.dst_context["_id"]}
        elif parent:
            create_doc[parent.level.name] = parent.dst_context["_id"]
        if c_level == "subject":
            create_doc.setdefault("code", create_doc.get("label"))

        fw_id = create_fn(create_doc)
        log.debug(f"Created {c_level} container: {create_doc} as {fw_id}")

        # update container with dst_context and dst_path
        container.dst_context = copy.deepcopy(container.src_context)
        container.dst_context["_id"] = fw_id
        parent_dst_path = parent.dst_path if parent else ""
        container.dst_path = fs.path.combine(
            parent_dst_path,
            utils.get_path_el(c_level, container.dst_context, use_labels=True)
        )
        self.update_containers.push({
            "id": container.id,
            "dst_context": container.dst_context,
            "dst_path": container.dst_path,
        })

    def _get_parents(self, container):
        parents = {}
        parent_id = container.parent_id
        while parent_id:
            parent = self.cache.get(parent_id)
            if not parent:
                parent = self.db.get_container(parent_id)
            parents[parent.id] = parent
            parent_id = parent.parent_id

        return parents

    def _should_skip_item(self, item: T.ItemWithErrorCount) -> bool:
        """Determine that item should be skipped or not"""
        if self.ingest_config.skip_existing and item.existing:
            log.debug(f"skip_existing: skipping item {item.id}")
            return True
        if self.ingest_config.detect_duplicates and item.error_cnt > 0:
            log.debug(f"detect_duplicates: skipping item {item.id}")
            return True
        return False

    def _on_success(self):
        # possible that no upload tasks were created - finalize
        self.db.start_finalizing()

    def _on_error(self):
        self.db.fail()
