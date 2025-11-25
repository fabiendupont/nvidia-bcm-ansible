from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ReportQuery(Entity):
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
                name="query",
                kind=MetaData.Type.STRING,
                description="Report query",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="description",
                kind=MetaData.Type.STRING,
                description="Description",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Notes",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="interval",
                kind=MetaData.Type.FLOAT,
                description="Interval",
                default=0,
            )
        )
        self.baseType = 'ReportQuery'
        self.service_type = self.baseType
        self.allTypes = ['ReportQuery']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

