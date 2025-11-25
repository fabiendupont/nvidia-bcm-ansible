from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MIGInformation(Entity):
    """
    Multi-Instance GPU information about the running instances
    """
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
                name="gpuId",
                kind=MetaData.Type.UINT,
                description="The hardware GPU identifier",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="profileId",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="instanceId",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="placementStart",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="placementSize",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memory",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="P2P",
                kind=MetaData.Type.BOOL,
                description="",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="SM",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="CE",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="DEC",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="JPEG",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ENC",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="OFA",
                kind=MetaData.Type.UINT,
                description="",
                default=0,
            )
        )
        self.baseType = 'MIGInformation'
        self.service_type = self.baseType
        self.allTypes = ['MIGInformation']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

