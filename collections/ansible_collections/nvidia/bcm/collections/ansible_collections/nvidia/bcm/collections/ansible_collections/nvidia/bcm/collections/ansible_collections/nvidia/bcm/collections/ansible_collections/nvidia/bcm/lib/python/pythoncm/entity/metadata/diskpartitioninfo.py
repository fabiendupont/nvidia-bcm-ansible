from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class DiskPartitionInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="The partition name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="majorID",
                kind=MetaData.Type.UINT,
                description="Major",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minorID",
                kind=MetaData.Type.UINT,
                description="Minor",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="blocks",
                kind=MetaData.Type.UINT,
                description="Blocks",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cipher",
                kind=MetaData.Type.STRING,
                description="Encryption cipher",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="slaves",
                kind=MetaData.Type.STRING,
                description="Slaves",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="deviceMapper",
                kind=MetaData.Type.STRING,
                description="Device mapper",
                default='',
            )
        )
        self.baseType = 'DiskPartitionInfo'
        self.service_type = self.baseType
        self.allTypes = ['DiskPartitionInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

