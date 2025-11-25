from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class HealthCheckForWlmJobOutput(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="measurable",
                kind=MetaData.Type.UUID,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="value",
                kind=MetaData.Type.FLOAT,
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="output",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="failed",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="reschedule",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.baseType = 'HealthCheckForWlmJobOutput'
        self.service_type = self.baseType
        self.allTypes = ['HealthCheckForWlmJobOutput']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

