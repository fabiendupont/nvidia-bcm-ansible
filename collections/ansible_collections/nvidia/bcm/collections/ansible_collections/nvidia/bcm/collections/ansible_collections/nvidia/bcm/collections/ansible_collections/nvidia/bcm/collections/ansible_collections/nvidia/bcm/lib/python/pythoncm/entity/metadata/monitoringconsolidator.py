from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringConsolidator(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disable, consolidator for all entities. Do not throw away existing data.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="consolidators",
                kind=MetaData.Type.ENTITY,
                description="Consolidators",
                instance='Consolidator',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringConsolidator'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringConsolidator']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

