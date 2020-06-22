# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.protect.rule.nosql_injection.mongo_nosql_scanner import (
    MongoNoSqlScanner,
)
from contrast.agent.protect.rule.sqli_rule import SqlInjection


class NoSqlInjection(SqlInjection):
    """
    NoSQL Injection Protection rule
    """

    NAME = "nosql-injection"

    def build_sample(self, context, evaluation, query, **kwargs):
        sample = self.build_base_sample(context, evaluation)
        if query is not None:
            sample.no_sqli.query = query

        if "start_idx" in kwargs:
            sample.no_sqli.start_idx = int(kwargs["start_idx"])

        if "end_idx" in kwargs:
            sample.no_sqli.end_idx = int(kwargs["end_idx"])

        if "boundary_overrun_idx" in kwargs:
            sample.no_sqli.boundary_overrun_idx = int(kwargs["boundary_overrun_idx"])

        if "input_boundary_idx" in kwargs:
            sample.no_sqli.input_boundary_idx = int(kwargs["input_boundary_idx"])

        return sample

    def get_database_scanner(self, database):
        return MongoNoSqlScanner()
