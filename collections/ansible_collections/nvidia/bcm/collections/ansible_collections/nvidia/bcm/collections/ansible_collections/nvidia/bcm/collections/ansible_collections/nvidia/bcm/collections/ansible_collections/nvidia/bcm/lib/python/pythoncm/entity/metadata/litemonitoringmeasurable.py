from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class LiteMonitoringMeasurable(Entity):
    """
    Lite monitoring measurable
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="producer",
                kind=MetaData.Type.UUID,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="parameter",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="kind",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cumulative",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.baseType = 'LiteMonitoringMeasurable'
        self.service_type = self.baseType
        self.allTypes = ['LiteMonitoringMeasurable']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

