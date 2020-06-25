"""Analyses init
"""
from dok8s.lib.analyses.component_analysis import ComponentAnalyser
from dok8s.lib.analyses.docker_analysis import DockerAnalyser
from dok8s.lib.analyses.resource_analysis import ResourceAnalyser

ANALYSES = [
    ComponentAnalyser,
    DockerAnalyser,
    ResourceAnalyser,
]
