from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KubePodInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="podNamespace",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="image",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.UUID,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.TIMESTAMP,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="labels",
                kind=MetaData.Type.STRING,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="reason",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="message",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ip",
                kind=MetaData.Type.STRING,
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="replicaSets",
                kind=MetaData.Type.STRING,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ready",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="volumes",
                kind=MetaData.Type.STRING,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="containers",
                kind=MetaData.Type.ENTITY,
                instance='ContainerInfo',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="creationTime",
                kind=MetaData.Type.TIMESTAMP,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="controllerId",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="resources",
                kind=MetaData.Type.STRING,
                description="List of requested (if pending) or allocated (if started) resources",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'KubePodInfo'
        self.service_type = self.baseType
        self.allTypes = ['KubePodInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

