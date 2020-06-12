""" Plugin implementations

This module contains the implementation of some features

- benchmarking
- pruning
"""
from mythril.laser.plugin.plugins.benchmark import BenchmarkPluginBuilder
from mythril.laser.plugin.plugins.coverage.coverage_plugin import CoveragePluginBuilder
from mythril.laser.plugin.plugins.dependency_pruner import DependencyPrunerBuilder
from mythril.laser.plugin.plugins.mutation_pruner import MutationPrunerBuilder
