"""Provides DetectDuplicatesTask class"""

from typing import Type

from flywheel.models import ContainerUidcheck

from .. import errors
from .. import models as M
from .. import schemas as T
from .abstract import Task


class DetectDuplicatesTask(Task):
    """Detecting duplicated data task"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.insert_errors = self.db.batch_writer_insert_error()
        self.update_containers = self.db.batch_writer_update_container()
        self.error_item_ids = []
        self.error_container_ids = set()

    def _run(self):
        self.report_progress(total=self.db.count_all_item())

        prev_item = None
        prev_item_conflict = False
        for item in self.db.get_items_sorted_by_dst_path():
            # filepath conflicts in Flywheel
            if item.existing:
                self._add_error(item, errors.DuplicateFilepathInFlywheel)

            # filepath conflicts in upload set
            if prev_item and prev_item.container_path == item.container_path and prev_item.filename == item.filename:
                self._add_error(item, errors.DuplicateFilepathInUploadSet)
                prev_item_conflict = True
            else:
                if prev_item_conflict:
                    # mark prev_item also as duplicate if we found any similar item
                    self._add_error(prev_item, errors.DuplicateFilepathInUploadSet)
                prev_item = item
                prev_item_conflict = False

            # update progress
            self.report_progress(completed=1)

        # check last prev_item
        # filepath conflict in upload set
        if prev_item_conflict:
            self._add_error(prev_item, errors.DuplicateFilepathInUploadSet)

        # check SOPInstanceUID duplicates
        item_ids = self.db.duplicated_sop_instance_uid_item_ids()
        self.error_item_ids.extend(item_ids)
        for item_id in item_ids:
            self.insert_errors.push(
                T.Error(item_id=item_id, code=errors.DuplicatedSOPInstanceUID.code).dict(exclude_none=True)
            )

        # container conflicts
        self._one_session_multi_study_uids()
        self._one_study_uid_multi_containers()
        self._one_acquisition_multi_series_uids()
        self._one_series_uid_multi_containers()

        # flywheel conflicts
        self._check_new_session_container_study_instance_uids()
        self._check_new_acquisition_container_study_instance_uids()

        # set the error flag for containers and child containers
        for containerid in self.db.find_all_containers_with_item_id(self.error_item_ids):
            self.error_container_ids.add(containerid.container_id)

        for container in self.db.get_all_container():
            if container.id in self.error_container_ids or container.parent_id in self.error_container_ids:
                self.update_containers.push({
                    "id": container.id,
                    "error": True
                })
                self.error_container_ids.add(container.id)
            # this might be needed only because of the test...might be good in the future
            if container.error:
                self.error_container_ids.add(container.id)

        self.insert_errors.flush()
        self.update_containers.flush()

    def _add_error(
        self,
        item: T.ItemWithContainerPath,
        error_type: Type[errors.BaseIngestError]
    ) -> None:
        """Add error for the specified item with the specified error type"""
        self.insert_errors.push(
            T.Error(item_id=item.id, code=error_type.code).dict(exclude_none=True)
        )

    def _on_success(self):
        self.db.set_ingest_status(status=T.IngestStatus.in_review)
        if self.ingest_config.assume_yes:
            # ingest was started with assume yes so accept the review
            self.db.review()

    def _on_error(self):
        self.db.fail()

    def _one_session_multi_study_uids(self):
        item_ids = self.db.one_session_container_multiple_study_instance_uid_item_ids()
        self.error_item_ids.extend(item_ids)

        for item_id in item_ids:
            self.insert_errors.push(
                T.Error(item_id=item_id, code=errors.DuplicatedStudyInstanceUID.code).dict(exclude_none=True)
            )

    def _one_study_uid_multi_containers(self):
        item_ids = self.db.one_study_instance_uid_multiple_session_container_item_ids()
        self.error_item_ids.extend(item_ids)

        for item_id in item_ids:
            self.insert_errors.push(
                T.Error(item_id=item_id, code=errors.DuplicatedStudyInstanceUIDInContainers.code).dict(exclude_none=True)
            )

    def _one_acquisition_multi_series_uids(self):
        item_ids = self.db.one_acquisition_container_multiple_series_instance_uid_item_ids()
        self.error_item_ids.extend(item_ids)

        for item_id in item_ids:
            self.insert_errors.push(
                T.Error(item_id=item_id, code=errors.DuplicatedSeriesInstanceUID.code).dict(exclude_none=True)
            )

    def _one_series_uid_multi_containers(self):
        item_ids = self.db.one_series_instance_uid_multiple_acquisition_container_item_ids()
        self.error_item_ids.extend(item_ids)

        for item_id in item_ids:
            self.insert_errors.push(
                T.Error(item_id=item_id, code=errors.DuplicatedSeriesInstanceUIDInContainers.code).dict(exclude_none=True)
            )

    def _check_new_session_container_study_instance_uids(self):
        """Check study instance uids in new session containers"""
        uids = self.db.study_instance_uids_in_new_session_container()
        if len(uids) < 1:
            return

        result = self.fw.check_uids_exist(
            ContainerUidcheck(
                sessions=list(uids)
            )
        )
        item_ids = set()
        for item in self.db.find_all_items_with_uid(M.UID.study_instance_uid.in_(result["sessions"])):
            self.error_item_ids.append(item.item_id)
            if not item.item_id in item_ids:
                self.insert_errors.push(
                    T.Error(item_id=item.item_id, code=errors.StudyInstanceUIDExists.code).dict(exclude_none=True)
                )
                item_ids.add(item.item_id)
                self.error_container_ids.add(item.acquisition_container_id)
                self.error_container_ids.add(item.session_container_id)


    def _check_new_acquisition_container_study_instance_uids(self):
        """Check series instance uids in new acquisition containers"""
        uids = self.db.series_instance_uids_in_new_acquisition_container()
        if len(uids) < 1:
            return

        result = self.fw.check_uids_exist(
            ContainerUidcheck(
                acquisitions=list(uids)
            )
        )
        item_ids = set()
        for item in self.db.find_all_items_with_uid(M.UID.series_instance_uid.in_(result["acquisitions"])):
            self.error_item_ids.append(item.item_id)
            if not item.item_id in item_ids:
                self.insert_errors.push(
                    T.Error(item_id=item.item_id, code=errors.SeriesInstanceUIDExists.code).dict(exclude_none=True)
                )
                item_ids.add(item.item_id)
                self.error_container_ids.add(item.acquisition_container_id)
