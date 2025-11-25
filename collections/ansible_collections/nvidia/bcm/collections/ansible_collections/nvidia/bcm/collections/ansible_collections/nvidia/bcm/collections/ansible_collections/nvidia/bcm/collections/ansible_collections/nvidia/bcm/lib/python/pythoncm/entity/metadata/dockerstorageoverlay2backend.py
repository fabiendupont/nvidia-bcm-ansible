from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.dockerstoragebackend import DockerStorageBackend


class DockerStorageOverlay2Backend(DockerStorageBackend):
    """
    Overlay2 is a modern union filesystem.
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="overrideKernelCheck",
                kind=MetaData.Type.BOOL,
                description="Override the kernel check to allow overlay2",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.STRING,
                description="Default max size of the container (empty = unlimited)",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Extra options used for the Overlay2 storage backend",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'DockerStorageBackend'
        self.childType = 'DockerStorageOverlay2Backend'
        self.service_type = self.baseType
        self.allTypes = ['DockerStorageOverlay2Backend', 'DockerStorageBackend']
        self.top_level = False
        self.leaf_entity = True

