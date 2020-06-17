"""Provides DicomScanner class."""

import copy
import gzip
import itertools
import logging
import os
import typing

import fs
from flywheel_migration.dcm import DicomFile
from pydicom.datadict import tag_for_keyword
from pydicom.multival import MultiValue
from pydicom.tag import Tag

from ... import util
from .. import deid, errors
from .. import schemas as T
from .abstract import AbstractScanner

log = logging.getLogger(__name__)

# Specifying just the list of tags we're interested in speeds up dicom scanning
DICOM_TAGS = [
    "Manufacturer",
    "AcquisitionNumber",
    "AcquisitionDate",
    "AcquisitionTime",
    "SeriesDate",
    "SeriesTime",
    "SeriesInstanceUID",
    "ImageType",
    "StudyDate",
    "StudyTime",
    "StudyInstanceUID",
    "OperatorsName",
    "PatientName",
    "PatientID",
    "StudyID",
    "SeriesDescription",
    "PatientBirthDate",
    "SOPInstanceUID",
]


class DicomScanner(AbstractScanner):
    """Scanner class to scan dicom files and create appropriate ingest items."""

    scanner_type = "dicom"
    # The session label dicom header key
    session_label_key = "StudyDescription"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.related_acquisitions = False
        self.sessions = {}
        self.deid_profile = None

    def _initialize(self):
        """Initiliate the scanner"""
        if self.ingest_config.de_identify:
            # inizialize deid profile
            self.deid_profile = deid.load_deid_profile(
                self.ingest_config.deid_profile,
                self.ingest_config.deid_profiles,
            ).get_file_profile("dicom")

    def _scan(self, subdir):
        """Scan all files in the given walker"""
        tags = [Tag(tag_for_keyword(keyword)) for keyword in DICOM_TAGS]

        for fileinfo in self.iter_files(subdir, report_progress=True):
            filepath = fs.path.combine(subdir, fileinfo.name)
            with self.walker.open(filepath, "rb", buffering=self.worker_config.buffer_size) as fileobj:
                try:
                    self.scan_dicom_file(filepath, fileobj, tags, size=fileinfo.size)
                except ValueError as exc:
                    log.debug(f"Skipped file {filepath} because {str(exc)}")
                    self.file_errors.append(T.Error(
                        code=errors.InvalidDicomFile.code,
                        message=str(exc),
                        filepath=filepath,
                    ))

        # TODO: consider memory usage in case of huge dataset
        for session in self.sessions.values():
            session_context = copy.deepcopy(self.context)
            session_context.update(session.context)

            session_uid = session.context["session"]["uid"]

            for acquisition in itertools.chain(session.acquisitions.values(), session.secondary_acquisitions.values()):
                acquisition_context = copy.deepcopy(session_context)
                acquisition_context.update(acquisition.context)

                series_uid = acquisition.context["acquisition"]["uid"]

                for series_uid, files in acquisition.files.items():
                    size = sum([filesize for _, filesize in files.values()])
                    file_paths = [fs.path.relpath(filepath) for filepath, _ in files.values()]
                    common_path = os.path.commonpath(file_paths)
                    file_paths = [fs.path.relpath(f.replace(common_path, "")) for f in file_paths]
                    filename = acquisition.filenames.get(series_uid)

                    packfile_context = copy.deepcopy(acquisition_context)
                    packfile_context["packfile"] = {
                        "type": "dicom",
                        "flatten": True,
                    }

                    item_with_uids = T.ItemWithUIDs(
                        item=T.ItemIn(
                            type="packfile",
                            dir=common_path,
                            files=file_paths,
                            filename=filename,
                            files_cnt=len(files),
                            bytes_sum=size,
                            context=packfile_context,
                        ),
                        uids=[]
                    )

                    for sop_uid in files:
                        try:
                            series_uid, acquisition_number = series_uid.rsplit("_", maxsplit=1)
                        except ValueError:
                            acquisition_number = None

                        item_with_uids.uids.append(
                            T.UIDIn(
                                item_id=item_with_uids.item.id,
                                study_instance_uid=session_uid,
                                series_instance_uid=series_uid,
                                acquisition_number=acquisition_number,
                                sop_instance_uid=sop_uid,
                                filename=files[sop_uid][0]
                            )
                        )

                    yield item_with_uids

    def scan_dicom_file(self, path, fp, tags, size=0):
        """Scan a single dicom file

        Args:
            path   (str): File path
            fp     (BinaryIO): File like object
            tags   (list): Dicom tags
            walker (AbstractWalker): Filesystem walker object

        """
        _, ext = os.path.splitext(path)
        if ext.lower() == ".gz":
            fp = gzip.GzipFile(fileobj=fp)

        # Don't decode while scanning, stop as early as possible
        # TODO: will we ever rely on fields after stack id for subject mapping
        if self.related_acquisitions:
            stop_function = stop_at_key((0x3006, 0x0011))
        else:
            stop_function = stop_at_key((0x0020, 0x9056))

        dcm = DicomFile(
            fp,
            parse=False,
            session_label_key=self.session_label_key,
            decode=self.related_acquisitions,
            stop_when=stop_function,
            update_in_place=False,
            specific_tags=tags,
            force=util.is_dicom_file(path),
        )

        acquisition = self.resolve_acquisition(self.context, dcm)
        series_uid = self.get_value(dcm, "SeriesInstanceUID", required=True)
        sop_uid = self.get_value(dcm, "SOPInstanceUID", required=True)
        acquisition_number = self.get_value(dcm, "AcquisitionNumber")
        if acquisition_number and int(acquisition_number) > 1:
            series_uid = f"{series_uid}_{int(acquisition_number)}"

        acquisition.files.setdefault(series_uid, {})
        acquisition.files[series_uid][sop_uid] = (path, size)

        if series_uid not in acquisition.filenames:
            acquisition_timestamp = self.determine_acquisition_timestamp(
                dcm
            )
            series_label = self.determine_acquisition_label(
                acquisition.context,
                dcm,
                series_uid,
                timestamp=acquisition_timestamp,
            )
            filename = self.determine_dicom_zipname(acquisition.filenames, series_label)
            acquisition.filenames[series_uid] = filename

    @staticmethod
    def determine_dicom_zipname(filenames, series_label):
        """Return a filename for the dicom series that is unique to a container

        Args:
            filenames (dict): A map of series uids to filenames
            series_label (str): The base to use for the filename

        Returns:
            str: The filename for the zipped up series
        """
        filename = series_label + ".dicom.zip"
        duplicate = 1
        while filename in filenames.values():
            filename = series_label + f"_dup-{duplicate}.dicom.zip"
            duplicate += 1
        return filename

    def resolve_session(self, context, dcm):
        """Find or create a sesson from a dcm file. """
        session_uid = self.get_value(dcm, "StudyInstanceUID", required=True)
        if session_uid not in self.sessions:
            subject_label = context.get("subject", {}).get("label")
            # Map subject
            if subject_label:
                subject_code = subject_label
            elif self.get_subject_code_fn and self.ingest_config.subject_config:
                fields = [self.extract_field(dcm, field) for field in self.ingest_config.subject_config.map_keys]
                subject_code = self.get_subject_code_fn(fields)
            else:
                subject_code = self.get_value(dcm, "PatientID", "")

            session_timestamp = self.get_timestamp(dcm, "StudyDate", "StudyTime")

            # Create session
            self.sessions[session_uid] = DicomSession(
                {
                    "session": {
                        "uid": session_uid,
                        "label": self.determine_session_label(
                            context, dcm, session_uid, timestamp=session_timestamp
                        ),
                        "timestamp": session_timestamp,
                        "timezone": str(util.DEFAULT_TZ),
                    },
                    "subject": {"label": subject_code},
                }
            )
        return self.sessions[session_uid]

    def resolve_acquisition(self, context, dcm):
        """Find or create an acquisition from a dcm file. """
        session = self.resolve_session(context, dcm)
        series_uid = self.get_value(dcm, "SeriesInstanceUID", required=True)
        primary_acquisition_file = True

        if self.related_acquisitions and dcm.get("ReferencedFrameOfReferenceSequence"):
            # We need to add it to the acquisition of the primary series uid
            try:
                series_uid = (
                    dcm.get("ReferencedFrameOfReferenceSequence")[0]
                    .get("RTReferencedStudySequence")[0]
                    .get("RTReferencedSeriesSequence")[0]
                    .get("SeriesInstanceUID")
                )
                primary_acquisition_file = False
            except (TypeError, IndexError, AttributeError):
                log.warning(
                    "Unable to find related series for file {}. Uploading into its own acquisition"
                )

        acquisition_number = self.get_value(dcm, "AcquisitionNumber")
        if acquisition_number and int(acquisition_number) > 1:
            series_uid = f"{series_uid}_{int(acquisition_number)}"

        if series_uid not in session.acquisitions:
           # full acquisition doesn't exists
            if (not primary_acquisition_file and series_uid in session.secondary_acquisitions):
                # The secondary acquisition exists
                return session.secondary_acquisitions[series_uid]

            acquisition_timestamp = self.determine_acquisition_timestamp(dcm)
            acquisition = DicomAcquisition(
                {
                    "acquisition": {
                        "uid": series_uid,
                        "label": self.determine_acquisition_label(
                            context, dcm, series_uid, timestamp=acquisition_timestamp
                        ),
                        "timestamp": acquisition_timestamp,
                        "timezone": str(util.DEFAULT_TZ),
                    }
                }
            )

            if primary_acquisition_file:
                # Check for a secondary and add it the files and filenames to the primary
                if series_uid in session.secondary_acquisitions:
                    acquisition.files = session.secondary_acquisitions.get(
                        series_uid
                    ).files
                    acquisition.filenames = session.secondary_acquisitions.pop(
                        series_uid
                    ).filenames

                session.acquisitions[series_uid] = acquisition
                return session.acquisitions[series_uid]
            session.secondary_acquisitions[series_uid] = acquisition
            return session.secondary_acquisitions[series_uid]

        # Acquisition already exists
        return session.acquisitions[series_uid]

    def determine_session_label(self, context, _dcm, uid, timestamp=None):  # pylint: disable=no-self-use
        """Determine session label from DICOM headers"""
        session_label = context.get("session", {}).get("label")
        if session_label:
            return session_label

        if timestamp:
            return timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return uid

    def determine_acquisition_label(self, context, dcm, uid, timestamp=None):
        """Determine acquisition label from DICOM headers"""
        acquisition_label = context.get("acquisition", {}).get("label")
        if acquisition_label:
            return acquisition_label

        name = self.get_value(dcm, "SeriesDescription")
        if not name and timestamp:
            name = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if not name:
            name = uid
        if isinstance(name, MultiValue):
            name = "_".join(name)
        return name

    def determine_acquisition_timestamp(self, dcm):
        """Get acquisition timestamp (based on manufacturer)"""
        # Create the acquisition because the acqusition doesn't exist
        if dcm.get_manufacturer() == "SIEMENS":
            timestamp = self.get_timestamp(dcm, "SeriesDate", "SeriesTime")
        else:
            timestamp = self.get_timestamp(dcm, "AcquisitionDate", "AcquisitionTime")
        return timestamp

    def get_timestamp(self, dcm, date_key, time_key):
        """Get a timestamp value"""
        date_value = self.get_value(dcm, date_key)
        time_value = self.get_value(dcm, time_key)

        return DicomFile.timestamp(date_value, time_value, util.DEFAULT_TZ)

    def get_value(self, dcm, key, default=None, required=False):
        """Get a transformed value"""
        if self.deid_profile:
            result = self.deid_profile.get_value(None, dcm.raw, key)
            if not result:
                result = default
        else:
            result = dcm.get(key, default)

        if result in [None, ""] and required:  # Explicit compare because zero is a valid value
            raise ValueError(f"DICOM is missing {key}")

        return result

    @staticmethod
    def extract_field(record, fieldname):
        """Extract field from record, and normalize it (by converting to lowercase and stripping whitespace)

        Args:
            record: A dictionary-like object
            fieldname (str): The field to extract

        Returns:
            str: The normalized value
        """
        value = record.get(fieldname, '')
        return str(value).strip().lower()


class DicomSession:
    """Dicom session class"""

    # pylint: disable=too-few-public-methods
    def __init__(self, context):
        """Helper class that holds session properties and acquisitions"""
        self.context = context
        self.acquisitions = {}
        self.secondary_acquisitions = {}  # Acquisitions that we don't have all
        # of the info for yet


class DicomAcquisition:
    """Dicom acquisition class"""

    # pylint: disable=too-few-public-methods
    def __init__(self, context):
        """Helper class that holds acquisition properties and files"""
        self.context = context
        self.files = (
            {}
        )  # Map of primary_series_uids to maps of series uids to filepaths
        # So that the primary series uid can be used to group multiple dicom series into one acquisition
        self.filenames = {}  # A map of series uid to filenames


def stop_at_key(key: typing.Any):
    """Return stop_when function for given DICOM tag"""
    stop_tag = Tag(key)

    def stop_when(tag: Tag, *_):
        """Return True if the current tag equals the stop_tag"""
        return tag == stop_tag

    return stop_when
