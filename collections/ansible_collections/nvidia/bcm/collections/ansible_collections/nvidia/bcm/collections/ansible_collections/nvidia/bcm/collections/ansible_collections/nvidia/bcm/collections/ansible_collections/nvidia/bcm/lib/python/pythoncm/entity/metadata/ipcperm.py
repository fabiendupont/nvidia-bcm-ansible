from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class IPCPerm(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="key",
                kind=MetaData.Type.INT,
                description="Message queue ID",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mode",
                kind=MetaData.Type.UINT,
                description="Access permissions",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="uid",
                kind=MetaData.Type.INT,
                description="Owner ID",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gid",
                kind=MetaData.Type.INT,
                description="Owner group ID",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="owner",
                kind=MetaData.Type.STRING,
                description="Owner",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="group",
                kind=MetaData.Type.STRING,
                description="Group name",
                readonly=True,
                default='',
            )
        )
        self.baseType = 'IPCPerm'
        self.service_type = self.baseType
        self.allTypes = ['IPCPerm']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

