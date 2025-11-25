from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class OCIGPUMemoryFabric(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="id",
                kind=MetaData.Type.STRING,
                description="Id.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="compartment_id",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="compute_hpc_island_id",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="compute_local_block_id",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="compute_network_block_id",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="fabric_health",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="lifecycle_state",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="time_created",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="total_host_count",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="healthy_host_count",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.baseType = 'OCIGPUMemoryFabric'
        self.service_type = self.baseType
        self.allTypes = ['OCIGPUMemoryFabric']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'
        self.add_to_cluster = False
        self.allow_commit = False

