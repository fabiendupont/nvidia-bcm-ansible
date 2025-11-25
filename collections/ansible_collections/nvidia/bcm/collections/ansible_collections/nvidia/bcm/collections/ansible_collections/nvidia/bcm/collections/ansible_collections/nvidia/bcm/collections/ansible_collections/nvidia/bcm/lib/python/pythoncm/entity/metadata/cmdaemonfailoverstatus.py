from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CMDaemonFailoverStatus(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_head_node_uuid",
                kind=MetaData.Type.UUID,
                description="Head node to which handeled request",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_active_head_node_uuid",
                kind=MetaData.Type.UUID,
                description="Active head node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="failoverId",
                kind=MetaData.Type.UINT,
                description="Head node with the highest failover ID will be active",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="error",
                kind=MetaData.Type.BOOL,
                description="Head node is in error state",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="peers",
                kind=MetaData.Type.ENTITY,
                description="Peer status per head node in the failover group",
                instance='CMDaemonFailoverPeer',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'CMDaemonFailoverStatus'
        self.service_type = self.baseType
        self.allTypes = ['CMDaemonFailoverStatus']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

