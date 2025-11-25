from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Semaphore(Entity):
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
                name="semid",
                kind=MetaData.Type.INT,
                description="Semaphore Set ID",
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
                name="nsems",
                kind=MetaData.Type.UINT,
                description="Number of semaphores in the set",
                readonly=True,
                default=0,
            )
        )
        self.baseType = 'Semaphore'
        self.service_type = self.baseType
        self.allTypes = ['Semaphore']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

