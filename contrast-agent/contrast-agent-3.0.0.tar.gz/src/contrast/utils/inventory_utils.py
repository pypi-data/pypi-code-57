# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.api.dtm_pb2 import ArchitectureComponent, LibraryUsageUpdate


class InventoryUtils(object):
    """
    Utility class to add inventory items to an ApplicationActivity object
    """

    @staticmethod
    def append_libraries(activity, settings):
        if not settings.config.get("inventory.enable", True):
            return

        for library in settings.libraries:
            usage = LibraryUsageUpdate()
            usage.hash_code = library.hash_code
            usage.count = library.used_class_count

            activity.library_usages[library.hash_code].CopyFrom(usage)

    @staticmethod
    def append_db_config(activity, obj):
        items = InventoryUtils.build_from_db_settings(obj)

        if len(items) > 0:
            activity.technologies["Database"] = True

            for item in items:
                activity.architectures.extend([item])
                activity.technologies[item.vendor] = True

    @staticmethod
    def build_from_db_settings(obj):
        if not obj:
            return []

        if isinstance(obj, dict):
            results = InventoryUtils._build_from_dict(obj)
        elif isinstance(obj, str):
            results = InventoryUtils._build_from_str(obj)
        else:
            raise Exception(
                "Unsupported database settings type of {}".format(type(obj).__name__)
            )

        return results

    @staticmethod
    def _build_from_dict(obj):
        """
        Builds ArchitectureComponent from dict
        """
        arch_comp = ArchitectureComponent()

        if "adapter" in obj and obj["adapter"]:
            arch_comp.vendor = obj["adapter"]

        if "host" in obj and obj["host"]:
            arch_comp.remote_host = obj["host"]

        if "port" in obj and obj["port"]:
            port = obj["port"]
            arch_comp.remote_port = int(port) if port else -1

        arch_comp.type = "db"
        arch_comp.url = obj["database"] if "database" in obj else "default"

        return [arch_comp]

    @staticmethod
    def _build_from_str(obj):
        """
        Builds ArchitectureComponent from database url string
        """

        adapter, obj = obj.split("://")
        _, obj = obj.split("@")
        hosts, db_and_options = obj.split("/")

        if "?" in db_and_options:
            database, _ = db_and_options.split("?")
        else:
            database = db_and_options

        if not hosts:
            hosts += "localhost"

        results = []

        for param in hosts.split(","):
            if ":" in param:
                host, port = param.split(":")
            else:
                host = param
                port = None

            arch_comp = ArchitectureComponent()

            arch_comp.vendor = adapter
            arch_comp.remote_host = host
            if port is not None:
                arch_comp.remote_port = int(port)
            arch_comp.type = "db"
            arch_comp.url = database

            results.append(arch_comp)

        return results

    @staticmethod
    def merge(item, other):
        if isinstance(other, dict):
            return  # TODO remove after accumulators

        for browser in other.browsers:
            item.browsers[browser] = True

        for tech in other.technologies:
            item.technologies[tech] = True

        for url in other.urls:
            item.urls[url] = True

        for library in other.libraries:
            item.library_usages[library.hash_code] = True

        # TODO: current de-duping happens in the service, but it might be more efficient to do it here, too
        for arch in other.architectures:
            item.architectures.add(arch)

        item.queries += other.queries
        item.url_count += other.url_count

        item.activity_duration_ms = max(
            [item.activity_duration_ms, other.activity_duration_ms]
        )
