import forge_template.paths as paths
from forge_template.config_generator import FileType
from forge_template.handler.databricks_handler import DatabricksHandler
from forge_template.tool_info import SchemaInfo, ToolInfo


class ConstList:
    @classmethod
    def get_attrs(cls):
        return [
            a for a in dir(cls) if (not a.startswith("_") and a not in ("get_attrs", "get_values", "get_attr_to_value"))
        ]

    @classmethod
    def get_values(cls):
        return [getattr(cls, a) for a in cls.get_attrs()]

    @classmethod
    def get_attr_to_value(cls):
        return {a: getattr(cls, a) for a in cls.get_attrs()}


class Tools(ConstList):
    DATABRICKS = ToolInfo(
        name="databricks",
        handler=DatabricksHandler,
        schema_info=[
            SchemaInfo(
                schema_path=paths.YAML_CONFIG_SCHEMA_PATH,
                output_path=paths.YAML_CONFIG_PATH,
                post_transforms=[
                    lambda s, p: s.replace("<PROJECT_NAME>", p),
                    lambda s, p: s.replace("<DB_PROJECT_NAME>", p.replace("-", "_")),
                ],
            ),
            SchemaInfo(
                schema_path=paths.YAML_SECRETS_SCHEMA_PATH,
                output_path=paths.YAML_SECRETS_PATH,
                post_transforms=[lambda s, p: s.replace("<PROJECT_NAME>", p)],
            ),
        ],
        github_actions_script_path=paths.DATABRICKS_SCRIPT_TEMPLATE_PATH,
        github_actions_template_path=paths.DATABRICKS_WORKFLOW_TEMPLATE_PATH,
        assert_match=True,
        assert_scope_match=True,
        file_type=FileType.YAML,
    )
    # SA_REPLICATION = ToolInfo(
    #     name="SA Replication",
    #     handler=SAReplicationHandler,
    #     schema_info=[],
    #     assert_scope_match=False,
    #     assert_match=False
    # )
    # POWERBI = ToolInfo(
    #     name="powerbi",
    #     handler=PowerBIHandler,
    #     schema_info=[
    #         SchemaInfo(schema_path=YAML_CONFIG_SCHEMA_PATH, output_path=YAML_CONFIG_PATH),
    #         SchemaInfo(schema_path=YAML_SECRETS_SCHEMA_PATH, output_path=YAML_SECRETS_PATH),
    #     ],
    #     github_actions_script_name=POWERBI_SCRIPT_NAME,
    #     github_actions_template_name=POWERBI_WORKFLOW_TEMPLATE_NAME,
    #     assert_match=True,
    #     assert_scope_match=True,
    # )
