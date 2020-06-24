from tktl.core import ExtendedEnum


class UserRepoConfigFileNameT(str, ExtendedEnum):
    YAML = "tktl.yaml"
    YML = "tktl.yml"


class UserProjectFileT(str, ExtendedEnum):
    FILE = "file"
    DIRECTORY = "dir"


class RequiredUserProjectPathsT(str, ExtendedEnum):
    SRC = "src"
    TKTL_YML = "tktl.yml"
    TKTL_YAML = "tktl.yaml"
    DOCKERFILE = "Dockerfile"
    REQS = "requirements.txt"

    @classmethod
    def strictly_required_files(cls):
        return {cls.DOCKERFILE.value, cls.REQS.value}

    @classmethod
    def strictly_required_dirs(cls):
        return {cls.SRC.value}


class DeploymentStatesT(ExtendedEnum):
    TEST_FAILED = "TEST_FAILED"
    IMAGE_BUILD_FAILED = "IMAGE_BUILD_FAILED"
    DEPLOYMENT_FAILED = "DEPLOYMENT_FAILED"
    CANCELED = "CANCELED"
    SUCCEED = "SUCCEED"
    TEST_RUNNING = "TEST_RUNNING"
    IMAGE_BUILDING = "IMAGE_BUILDING"
    DEPLOYING = "DEPLOYING"


class ProjectAssetT(str, ExtendedEnum):
    DATA = "DATA"
    MODEL = "MODEL"


class ProjectAssetSourceT(str, ExtendedEnum):
    S3 = "S3"
    LOCAL = "LOCAL"
    LFS = "LFS"


class EndpointT(str, ExtendedEnum):
    REST = "REST"
    GRPC = "GRPC"


class EndpointComputeT(str, ExtendedEnum):
    GPU = "GPU"
    CPU = "CPU"
