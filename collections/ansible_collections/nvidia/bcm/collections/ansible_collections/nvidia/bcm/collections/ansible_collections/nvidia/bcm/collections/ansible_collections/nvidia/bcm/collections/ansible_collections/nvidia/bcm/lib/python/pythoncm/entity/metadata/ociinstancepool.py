from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class OCIInstancePool(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="User-defined name of the instance pool",
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
                name="region",
                kind=MetaData.Type.RESOLVE,
                description="Region for instance",
                instance='OCIRegion',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="isClusterNetwork",
                kind=MetaData.Type.BOOL,
                description="Is instance pool a part of cluster network",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="instancePoolId",
                kind=MetaData.Type.STRING,
                description="Instance pool OCID (generated automatically by default)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="clusterNetworkId",
                kind=MetaData.Type.STRING,
                description="Cluster network OCID (if applicable, generated automatically by default)",
                default='',
            )
        )
        self.baseType = 'OCIInstancePool'
        self.service_type = self.baseType
        self.allTypes = ['OCIInstancePool']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

