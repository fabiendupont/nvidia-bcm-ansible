from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class OCIGPUMemoryCluster(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="User-defined name of the GMC",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="provider",
                kind=MetaData.Type.RESOLVE,
                description="Cloud provider",
                instance='CloudProvider',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="id",
                kind=MetaData.Type.STRING,
                description="OCID of this GPU memory cluster",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpuMemoryFabricId",
                kind=MetaData.Type.STRING,
                description="OCID of the GPU memory fabric to use",
                default='',
            )
        )
        self.baseType = 'OCIGPUMemoryCluster'
        self.service_type = self.baseType
        self.allTypes = ['OCIGPUMemoryCluster']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

