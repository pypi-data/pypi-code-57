import logging
import typing
import itertools

import eyed3

module_logger = logging.getLogger(__name__)

__all__ = [
    "BDSMetaDataType",
    "blue_dot_sessions_metadata",
    "get_blue_dot_sessions_metadata"
]


BDSMetaDataType = typing.Dict[str, int]


blue_dot_sessions_metadata = [
    "Mood",
    "Density",
    "Gravity",
    "Energy",
    "Ensemble",
    "Melody",
    "Tension",
    "Rhythm"
]


def get_blue_dot_sessions_metadata(
    file_path: str
) -> typing.Optional[BDSMetaDataType]:
    """
    Get Blue Dot Sessions characteristics from .mp3 file.

    Args:
        file_path (str): File path to .mp3 file

    Returns:
        dict: keys are `gemscapes.metadata.blue_dot_sessions_metadata`
            entries, and values are integer values corresponding to each
            metadata characteristic
    """
    id_locator = "ID:"
    audiofile = eyed3.load(file_path)
    module_logger.debug(f"get_blue_dot_sessions_metadata: audiofile={audiofile}")
    if audiofile.tag is None:
        return None

    for comment in itertools.chain(audiofile.tag.comments, audiofile.tag.user_text_frames):
        if id_locator in comment.text:
            start_idx = comment.text.find(id_locator)
            end_idx = comment.text.find(".", start_idx)
            characteristics = comment.text[start_idx + len(id_locator):end_idx]
            return {
                blue_dot_sessions_metadata[idx]: int(characteristics[idx])
                for idx in range(len(characteristics))
            }
    return None
