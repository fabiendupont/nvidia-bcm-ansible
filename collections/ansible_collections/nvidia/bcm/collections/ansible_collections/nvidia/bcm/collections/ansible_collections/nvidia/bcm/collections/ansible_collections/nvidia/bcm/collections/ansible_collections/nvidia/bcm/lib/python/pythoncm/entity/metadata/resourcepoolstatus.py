from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ResourcePoolStatus(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.UUID,
                description="Nodes",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeStatus",
                kind=MetaData.Type.INT,
                description="Node status",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="resources",
                kind=MetaData.Type.UUID,
                description="Resources",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="resourceStatus",
                kind=MetaData.Type.INT,
                description="Resource status",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="resourceMessages",
                kind=MetaData.Type.STRING,
                description="Resource message",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ResourcePoolStatus'
        self.service_type = self.baseType
        self.allTypes = ['ResourcePoolStatus']
        self.top_level = False
        self.leaf_entity = True

