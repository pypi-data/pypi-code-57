from __future__ import absolute_import, division, print_function

from openai import api_resources
from openai.api_resources.experimental.completion_config import CompletionConfig

OBJECT_CLASSES = {
    "branch": api_resources.Branch,
    "engine": api_resources.Engine,
    "experimental.completion_config": CompletionConfig,
    "plan": api_resources.Plan,
    "snapshot": api_resources.Snapshot,
    "tag": api_resources.Tag,
    "update": api_resources.Update,
}
