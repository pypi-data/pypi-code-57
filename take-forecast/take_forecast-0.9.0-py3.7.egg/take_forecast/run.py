# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.2.0'

from pathlib import Path
from typing import Dict

from kedro.context import KedroContext, load_context
from kedro.pipeline import Pipeline

from take_forecast.pipeline import create_pipelines


class ProjectContext(KedroContext):
	"""Context class for this project.
	
	Example:
	::
	>>> from take_forecast.run import ProjectContext
	>>> context = ProjectContext('project_path')
	>>> context.run()
	
	Or with file ``.kedro.yml`` specifying take_forecast context as project context
	::
		context_path: take_forecast.run.ProjectContext
	
	Example:
	::
	>>> from kedro.context import load_context
	>>> context = load_context('project_path')
	"""
	
	project_name = 'Forecast'
	project_version = '0.15.9'
	
	
	def _get_pipelines(self) -> Dict[str, Pipeline]:
		return create_pipelines()


def run_package():
	"""Run method to run default pipeline."""
	project_context = load_context(Path.cwd())
	project_context.run()


if __name__ == "__main__":
	run_package()
