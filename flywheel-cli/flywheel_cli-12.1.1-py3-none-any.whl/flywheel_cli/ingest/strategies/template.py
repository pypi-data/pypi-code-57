"""Provides TemplateIngestStrategy class."""
# pylint: disable=R0903
import re

from ..template import parse_template_list, parse_template_string
from .abstract import Strategy


class TemplateStrategy(Strategy):
    """Strategy to ingest a folder using a template"""

    def initialize(self):
        """Initialize the strategy."""
        if not self.config.template:
            raise ValueError(
                "Template must be specified, either with --template argument or in the config file"
            )
        if isinstance(self.config.template, str):
            # Build the template string
            try:
                self.root_node = parse_template_string(self.config)
            except (ValueError, re.error) as exc:
                raise ValueError(f"Invalid template: {exc}")
        else:
            self.root_node = parse_template_list(self.config)

        self.check_group_reference()

    def check_group_reference(self):
        """Check if template or config.group refer to group id"""
        if not self.config.group:
            node = self.root_node
            while node:
                if hasattr(node, "template") and "group" in node.template.pattern:
                    break
                node = getattr(node, "next_node", None)
            else:
                raise ValueError(
                    "Group must be specified either in the template or using -g"
                )
