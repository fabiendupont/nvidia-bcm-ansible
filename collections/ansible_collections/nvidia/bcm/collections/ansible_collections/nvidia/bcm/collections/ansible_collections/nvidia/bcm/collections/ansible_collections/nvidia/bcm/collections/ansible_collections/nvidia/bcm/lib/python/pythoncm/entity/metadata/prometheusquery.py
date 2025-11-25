from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PrometheusQuery(Entity):
    class Access(Enum):
        PUBLIC = auto()
        PRIVATE = auto()
        INDIVIDUAL = auto()

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
                name="alias",
                kind=MetaData.Type.STRING,
                description="Alternative name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="query",
                kind=MetaData.Type.STRING,
                description="PromQL Query",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="typeClass",
                kind=MetaData.Type.STRING,
                description="Type class, slash(/) separated for levels",
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
                name="startTime",
                kind=MetaData.Type.STRING,
                description="Default query start time",
                regex_check=r"^[0-9]+|now(([-+][0-9]+)+([smhdwMy]))?(/[smhdwMy])?$",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="endTime",
                kind=MetaData.Type.STRING,
                description="Default end start time",
                regex_check=r"^[0-9]*|now(([-+][0-9]+)+([smhdwMy]))?(/[smhdwMy])?$",
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
        self.meta.add(
            MetaDataField(
                name="cumulative",
                kind=MetaData.Type.BOOL,
                description="Use the cumulative value, not the latest counter",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="access",
                kind=MetaData.Type.ENUM,
                description="User access control",
                options=[
                    self.Access.PUBLIC,
                    self.Access.PRIVATE,
                    self.Access.INDIVIDUAL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Access,
                default=self.Access.PUBLIC,
            )
        )
        self.meta.add(
            MetaDataField(
                name="unit",
                kind=MetaData.Type.STRING,
                description="Unit of measure for the query results",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="price",
                kind=MetaData.Type.FLOAT,
                description="Optional price associtated with the query results per unit",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="currency",
                kind=MetaData.Type.STRING,
                description="Currency",
                default="$",
            )
        )
        self.meta.add(
            MetaDataField(
                name="preference",
                kind=MetaData.Type.UINT,
                description="The query with the highest preference be shown by default",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="drilldown",
                kind=MetaData.Type.ENTITY,
                description="Manage the drilldown queries",
                instance='PrometheusQueryDrilldown',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'PrometheusQuery'
        self.service_type = self.baseType
        self.allTypes = ['PrometheusQuery']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

