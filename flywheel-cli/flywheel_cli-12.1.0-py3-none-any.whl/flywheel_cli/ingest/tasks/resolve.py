"""Provides ResolveTask class."""

import logging
import os
import uuid

import flywheel
import fs

from ...util import str_to_filename
from .. import models as M
from .. import schemas as T
from .. import utils
from .abstract import Task


log = logging.getLogger(__name__)

CONTAINER_FIELDS = ["id", "label", "uid", "code"]


class ResolveTask(Task):
    """Resolve containers for review."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited = set()
        self.insert_containers = self.db.batch_writer_insert_container()
        self.update_items = self.db.batch_writer_update_item(depends_on=self.insert_containers)
        self.update_uids = self.db.batch_writer_update_uid(depends_on=self.insert_containers)
        # keep cache size in sync with the size of the batch writer
        # this simplify how we find the already resolved containers
        # otherwise we should check the batch writer buffer and if the item is
        # is not there query the db
        # How can cache miss happen?
        # item path order not equal with container path order
        self.cache = utils.LRUCache(self.insert_containers.batch_size)
        self.uid_ids = None

    def _run(self):
        self.report_progress(total=self.db.count_all_item())

        for item in self.db.get_all_item():
            container = self._resolve_item_containers(item)
            if not container:
                log.warning(f"Couldn't resolve container for: {item.id}")
                continue

            filename = item.filename or self._get_filename(item, container)
            dst_files = container.dst_context.get("files", []) if container.dst_context else []
            update = {
                "id": item.id,
                "container_id": container.id,
                "existing": filename in dst_files,
            }
            if filename != item.filename:
                update["filename"] = filename

            self.update_items.push(update)

            # update progress
            self.report_progress(completed=1)

        # flush all remaining items to the db
        self.update_items.flush()
        self.update_uids.flush()

    def _on_success(self):
        if self.ingest_config.detect_duplicates:
            self.db.start_detecting_duplicates()
        else:
            self.db.set_ingest_status(status=T.IngestStatus.in_review)
            if self.ingest_config.assume_yes:
                # ingest was started with assume yes so accept the review
                self.db.review()

    def _on_error(self):
        self.db.fail()

    def _get_uid_ids(self, item):
        if self.uid_ids is None:
            self.uid_ids = set()
            for uid in self.db.get_all_uid(M.UID.item_id == item.id):
                self.uid_ids.add(uid.id)
        return self.uid_ids

    def _resolve_item_containers(self, item):
        item_context = item.context
        last = None
        path = []
        uid_updates = {}
        self.uid_ids = None

        def add_update(uids, container_type, container_id):
            for uid in uids:
                if not uid in uid_updates:
                    uid_updates[uid] = {"id": uid}
                uid_updates[uid][container_type] = container_id

        for c_level in T.ContainerLevel:
            c_name = c_level.name
            if c_name in item_context:
                context = item_context[c_name]
                path.append(utils.get_path_el(c_name, context))
                current = self._resolve_container(c_level, path, context, last)

                if self.ingest_config.detect_duplicates:
                    uid_ids = self._get_uid_ids(item)
                    if current.level == T.ContainerLevel.session:
                        add_update(uid_ids, "session_container_id", current.id)

                    if current.level == T.ContainerLevel.acquisition:
                        add_update(uid_ids, "acquisition_container_id", current.id)

                if current:
                    last = current
                else:
                    break
            else:
                break

        for update in uid_updates.values():
            self.update_uids.push(update)

        return last

    def _resolve_container(self, c_level, path, context, parent):
        cid = context.get("_id")
        label = context.get("label")
        path_str = os.path.join(*path)

        if not (cid or label):
            return None

        if path_str in self.visited:
            # already created container with this path
            # try to get from cache
            child = self.cache.get(path_str)
            if not child:
                # if not in cache, get from database
                # make sure to flush the batch writer
                self.insert_containers.flush()
                child = self.db.find_one_container(M.Container.path == path_str)
                self.cache[path_str] = child
            return child

        # create new container node
        child = T.ContainerIn(
            id=uuid.uuid4(),
            path=path_str,
            level=c_level,
            src_context=context,
            parent_id=parent.id if parent else None,
        )

        if not parent or parent.dst_path:
            # try to resolve if parent exists
            target, dst_files = self._find_child_by_path(path)

            if target:
                child.existing = True
                child.dst_context = self.get_dst_context(target)
                child.dst_context["files"] = dst_files
                child.dst_path = utils.get_path_el(c_level.name, child.dst_context, use_labels=True)
                if parent:
                    child.dst_path = os.path.join(parent.dst_path, child.dst_path)

        log.debug(f"Resolved {c_level.name} container: {path_str}")
        self.visited.add(path_str)
        self.insert_containers.push(child.dict())
        self.cache[path_str] = child
        return child

    def _find_child_by_path(self, path):
        """Attempt to find the child."""
        try:
            container = self.fw.lookup(path)
            files = getattr(container, "files", [])
            files = list(map(lambda f: f.name, files))
            log.debug(f"Resolve: {path} - returned: {container.id}")
            return container, files
        except flywheel.ApiException:
            log.debug(f"Resolve: {path} - NOT FOUND")
            return None, None

    @staticmethod
    def get_dst_context(container):
        """Get metadata from flywheel container object returned by sdk."""
        src = container.to_dict()
        ctx = {key: src.get(key) for key in CONTAINER_FIELDS if src.get(key)}
        ctx["_id"] = ctx.pop("id")
        return ctx

    @staticmethod
    def _get_filename(item, container):
        if item.type == T.ItemType.packfile:
            if container.dst_context:
                label = container.dst_context.get("label")
            else:
                label = container.src_context.get("label")
            packfile_name = str_to_filename(label)
            if item.context["packfile"]["type"] == "zip":
                filename = f"{packfile_name}.zip"
            else:
                filename = f"{packfile_name}.{item.context['packfile']['type']}.zip"
        else:
            filename = fs.path.basename(item.files[0])
        return filename
