from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PrometheusQueryDrilldown(Entity):
    """
    Prometheus query drill down
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="The name of the drill down",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="parameters",
                kind=MetaData.Type.STRING,
                description="Parameters to be passed to the drill down query",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="query",
                kind=MetaData.Type.RESOLVE,
                description="Query to execute",
                instance='PrometheusQuery',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'PrometheusQueryDrilldown'
        self.service_type = self.baseType
        self.allTypes = ['PrometheusQueryDrilldown']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

