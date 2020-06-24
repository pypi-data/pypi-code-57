from typing import Union, List

from pydantic import BaseModel

from tktl.core.t import ProjectAssetT, ProjectAssetSourceT, EndpointComputeT, EndpointT


class ProjectContentsBase(BaseModel):
    type: str
    name: str
    path: str


class ProjectFile(ProjectContentsBase):
    type: str = "file"


class ProjectFileWithContent(ProjectContentsBase):
    type: str = "file"
    content: str


class ProjectDirectory(ProjectContentsBase):
    type: str = "dir"


class ProjectAsset(ProjectContentsBase):
    calculated_sha: str
    kind: ProjectAssetT
    source: ProjectAssetSourceT
    requires_download: bool


class TktlServiceConfigSchema(BaseModel):
    replicas: int
    compute_type: EndpointComputeT
    endpoint_type: EndpointT


class TktlAssetConfigSchema(BaseModel):
    path: str
    version: int


class TktlYamlConfigSchema(BaseModel):

    """
    default_branch_name: master
    service:

      replicas: 2
      compute_type: CPU
      endpoint_type: REST

    model:
      path: assets/model.pkl
      version: 1

    data:
      path: assets/data.pkl
      version: 1

    """

    default_branch_name: str
    service: TktlServiceConfigSchema
    model: TktlAssetConfigSchema
    data: TktlAssetConfigSchema


class TktlYamlConfigValidationError(BaseModel):
    loc: str
    msg: str


class ProjectValidationOutput(BaseModel):
    title: str
    summary: str
    text: str


ProjectContentSingleItemT = Union[ProjectFile, ProjectDirectory]
ProjectContentMultiItemT = List[ProjectContentSingleItemT]
ProjectContentT = Union[
    ProjectContentSingleItemT, ProjectContentMultiItemT, ProjectFileWithContent
]
