from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class OSCloudExtension(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="User-defined name of the private cloud",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="region",
                kind=MetaData.Type.RESOLVE,
                description="Region of the cluster extension",
                instance='OSCloudRegion',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="network",
                kind=MetaData.Type.RESOLVE,
                description="Network associated with the extension",
                clone=False,
                instance='Network',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="floatingIpNetworkId",
                kind=MetaData.Type.STRING,
                description="Floating IP Network UUID or name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="stackId",
                kind=MetaData.Type.STRING,
                description="Heat stack ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultDirectorSecGroupId",
                kind=MetaData.Type.STRING,
                description="Default security group ID/name for the cloud director",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultCnodeSecGroupId",
                kind=MetaData.Type.STRING,
                description="Default security group ID/name for the cloud nodes",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraField",
                kind=MetaData.Type.STRING,
                description="A list of various advanced options",
                clone=False,
                vector=True,
                default=[],
            )
        )
        self.baseType = 'OSCloudExtension'
        self.service_type = self.baseType
        self.allTypes = ['OSCloudExtension']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

