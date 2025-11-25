from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class HealthCheckForWlmJobResult(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="hostname",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="job_id",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="output",
                kind=MetaData.Type.ENTITY,
                instance='HealthCheckForWlmJobOutput',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'HealthCheckForWlmJobResult'
        self.service_type = self.baseType
        self.allTypes = ['HealthCheckForWlmJobResult']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

