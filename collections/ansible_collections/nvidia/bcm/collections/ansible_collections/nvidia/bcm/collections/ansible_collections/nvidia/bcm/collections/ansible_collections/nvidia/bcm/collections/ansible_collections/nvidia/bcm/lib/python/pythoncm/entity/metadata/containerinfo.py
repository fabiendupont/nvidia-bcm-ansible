from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ContainerInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="The name of the container",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="containerId",
                kind=MetaData.Type.STRING,
                description="The id",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="image",
                kind=MetaData.Type.STRING,
                description="The name of the image",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="imageId",
                kind=MetaData.Type.STRING,
                description="The sha id of the image",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.STRING,
                description="The state of the container",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.TIMESTAMP,
                description="The time when the container started",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="lastTerminationState",
                kind=MetaData.Type.STRING,
                description="The last state when the container terminated",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="reason",
                kind=MetaData.Type.STRING,
                description="The reason for the termination",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="lastExitCode",
                kind=MetaData.Type.INT,
                description="The exit code of the container",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="previousStartTime",
                kind=MetaData.Type.TIMESTAMP,
                description="The previous start time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="previousFinishTime",
                kind=MetaData.Type.TIMESTAMP,
                description="The previous finish time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ready",
                kind=MetaData.Type.BOOL,
                description="Whether the container is ready or not",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="restartCount",
                kind=MetaData.Type.INT,
                description="The number of restarts of the container",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="environmentVariables",
                kind=MetaData.Type.STRING,
                description="The environment variables passed to the container",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ContainerInfo'
        self.service_type = self.baseType
        self.allTypes = ['ContainerInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

