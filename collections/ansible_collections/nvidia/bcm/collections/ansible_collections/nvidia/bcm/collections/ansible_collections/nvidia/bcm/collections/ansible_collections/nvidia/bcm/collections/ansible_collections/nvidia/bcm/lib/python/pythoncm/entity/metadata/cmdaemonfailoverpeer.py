from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CMDaemonFailoverPeer(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_head_node_uuid",
                kind=MetaData.Type.UUID,
                description="Head node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.STRING,
                description="Status",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="failCount",
                kind=MetaData.Type.INT,
                description="Number of sequencial times failure was detected",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'CMDaemonFailoverPeer'
        self.service_type = self.baseType
        self.allTypes = ['CMDaemonFailoverPeer']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

