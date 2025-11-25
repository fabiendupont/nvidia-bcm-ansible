from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MsgQueue(Entity):
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
                name="msqid",
                kind=MetaData.Type.INT,
                description="Message queue ID",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ipcperm",
                kind=MetaData.Type.ENTITY,
                description="IPC permissions",
                readonly=True,
                instance='IPCPerm',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Size in bytes",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="qnum",
                kind=MetaData.Type.UINT,
                description="Number of messages in the queue",
                readonly=True,
                default=0,
            )
        )
        self.baseType = 'MsgQueue'
        self.service_type = self.baseType
        self.allTypes = ['MsgQueue']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

