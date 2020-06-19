import typing
import logging
import inspect
import time

from ..metadata import get_blue_dot_sessions_metadata
from .convert import convert
from .wav2png import wav2png
from .post_wav2png import post_wav2png
from .primitive import primitive
from .post_primitive import post_primitive


__all__ = [
    "convert",
    "wav2png",
    "post_wav2png",
    "primitive",
    "post_primitive",
    "process_pipeline_stages",
    "pipeline",
    "pipeline_sig",
    "pipeline_stage_count",
    "pipeline_stage_names"
]


module_logger = logging.getLogger(__name__)


def process_pipeline_stages(stages_str: str) -> slice:
    module_logger.debug(f"process_pipeline_stages: stages_str={stages_str}")
    if ":" in stages_str:
        stages = []
        split = stages_str.split(":")
        for val in split:
            try:
                val = int(val)
            except ValueError:
                val = None
            stages.append(val)
        stages = slice(*stages)
    else:
        stages = slice(int(stages_str))
    module_logger.debug(f"process_pipeline_stages: stages={stages}")
    return stages


PipelineFnType = typing.Callable[[str, typing.Optional[bool]], str]

def pipeline(
    convert_fn: PipelineFnType,
    wav2png_fn: PipelineFnType,
    post_wav2png_fn: PipelineFnType,
    primitive_fn: PipelineFnType,
    post_primitive_fn: PipelineFnType
) -> PipelineFnType:
    """
    Run gemscape pipeline consisting of the following stages:

    conversion: Convert .mp3 input to .wav
    wav2png: Create a visual representation of .wav file
    post wav2png: Modify wav2png output before passing to primitive
    primtive: Call `primitive`, creating SVG from PNG
    post primitive: Modify primitive output

    Returns:
        function that takes as input .mp3 file.
    """

    def _time(fn, *args, **kwargs):
        t0 = time.time()
        res = fn(*args, **kwargs)
        delta = time.time() - t0
        return res, delta

    fns = [
        convert_fn,
        wav2png_fn,
        post_wav2png_fn,
        primitive_fn,
        post_primitive_fn
    ]

    fn_names = [
        "convert_fn",
        "wav2png_fn",
        "post_wav2png_fn",
        "primitive_fn",
        "post_primitive_fn"
    ]


    def _pipeline(file_path: str, stages: slice = None) -> str:

        track_metadata = get_blue_dot_sessions_metadata(file_path)
        module_logger.debug(f"pipeline._pipeline: track_metadata={track_metadata}")

        if stages is None:
            stages = slice(None)
        stages = range(len(fns))[stages]

        module_logger.debug(f"pipeline._pipeline: stages={stages}")

        for idx, fn in enumerate(fns):
            # module_logger.debug(f"pipeline._pipeline: idx={idx}, stages[-1]={stages[-1]}")
            if idx == stages[-1] + 1:
                break
            if idx < stages[0]:
                module_logger.debug(f"pipeline: stage {idx}, calling {fn_names[idx]}({file_path}, dry_run=True) ")
                file_path, delta = _time(fn, file_path, dry_run=True, track_metadata=track_metadata)
            else:
                module_logger.debug(f"pipeline: stage {idx}, calling {fn_names[idx]}({file_path})")
                file_path, delta = _time(fn, file_path, track_metadata=track_metadata)
            module_logger.debug(f"pipeline: stage {idx}, {fn_names[idx]} took {delta:.2f} sec")
            yield file_path

    return _pipeline


pipeline_sig = inspect.signature(pipeline)
pipeline_stage_count = len(pipeline_sig.parameters)
pipeline_stage_names = [param for param in pipeline_sig.parameters]
