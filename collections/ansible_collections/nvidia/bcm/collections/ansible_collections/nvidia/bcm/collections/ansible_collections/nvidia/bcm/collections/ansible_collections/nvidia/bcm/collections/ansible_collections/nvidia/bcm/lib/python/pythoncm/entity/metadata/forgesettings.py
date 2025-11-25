from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudsettings import CloudSettings


class ForgeSettings(CloudSettings):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="instanceId",
                kind=MetaData.Type.STRING,
                description="Instance ID in Forge",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="instanceType",
                kind=MetaData.Type.RESOLVE,
                description="Instance type",
                instance='ForgeInstanceType',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="machineId",
                kind=MetaData.Type.STRING,
                description="Forge Machine ID",
                clone=False,
                default='',
            )
        )
        self.baseType = 'CloudSettings'
        self.childType = 'ForgeSettings'
        self.service_type = self.baseType
        self.allTypes = ['ForgeSettings', 'CloudSettings']
        self.top_level = False
        self.leaf_entity = True

