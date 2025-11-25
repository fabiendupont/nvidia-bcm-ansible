from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CloudRegion(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="The name of the cloud region.",
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
                name="timeZoneSettings",
                kind=MetaData.Type.ENTITY,
                description="Time zone",
                instance='TimeZoneSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'CloudRegion'
        self.service_type = self.baseType
        self.allTypes = ['CloudRegion']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

