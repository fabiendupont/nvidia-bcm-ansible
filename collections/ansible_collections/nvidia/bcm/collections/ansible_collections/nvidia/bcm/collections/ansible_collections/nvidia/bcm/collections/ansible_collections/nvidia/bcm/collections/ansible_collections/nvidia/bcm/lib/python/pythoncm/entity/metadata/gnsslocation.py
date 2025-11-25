from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GNSSLocation(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_entity_uuid",
                kind=MetaData.Type.UUID,
                description="Entity",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="timestamp",
                kind=MetaData.Type.FLOAT,
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="latitude",
                kind=MetaData.Type.FLOAT,
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="longitude",
                kind=MetaData.Type.FLOAT,
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="height",
                kind=MetaData.Type.FLOAT,
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="message",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.baseType = 'GNSSLocation'
        self.service_type = self.baseType
        self.allTypes = ['GNSSLocation']
        self.top_level = False
        self.leaf_entity = True

