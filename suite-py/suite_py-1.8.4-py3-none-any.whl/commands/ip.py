# -*- coding: utf-8 -*-
import re

from pptree import Node, print_tree
from suite_py.lib.handler import aws_handler as aws
from suite_py.lib.logger import Logger

logger = Logger()


def entrypoint(project_name, env):

    clusters_names = aws.get_ecs_clusters(env)
    n_services = Node("services")

    projects = {
        "prima": ["web", "consumer"],
        "ab_normal": ["abnormal"],
    }
    project_names = projects.get(project_name, [project_name])

    for cluster_name in clusters_names:

        services = []
        all_services = aws.get_ecs_services(cluster_name)

        for service in all_services:
            if service["status"] == "ACTIVE":
                for prj in project_names:
                    if prj in service["serviceName"]:
                        services.append(service["serviceName"])

        for service in services:
            container_instances = []
            container_instances = aws.get_container_instances_arn_from_service(
                cluster_name, service
            )
            if container_instances:
                ips = aws.get_ips_from_container_instances(
                    cluster_name, container_instances
                )

                m = re.search(f"ecs-task-.*-{env}-ECSService(.*)-.*", service)
                if m:
                    n_service = Node(m.group(1), n_services)
                    for ip in ips:
                        Node(ip, n_service)

    print_tree(n_services, horizontal=True)
    logger.info("Done!")
