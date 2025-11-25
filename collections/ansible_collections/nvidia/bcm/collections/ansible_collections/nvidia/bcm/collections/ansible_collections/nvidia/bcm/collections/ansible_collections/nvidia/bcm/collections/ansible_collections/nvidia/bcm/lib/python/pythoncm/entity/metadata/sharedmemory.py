from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SharedMemory(Entity):
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
                name="shmid",
                kind=MetaData.Type.INT,
                description="Shared memory ID",
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
                name="cpid",
                kind=MetaData.Type.INT,
                description="Creator PID",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nattch",
                kind=MetaData.Type.INT,
                description="Number of attaches",
                readonly=True,
                default=0,
            )
        )
        self.baseType = 'SharedMemory'
        self.service_type = self.baseType
        self.allTypes = ['SharedMemory']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

