from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class JobQueueStat(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Queue name",
                required=True,
                diff_type=MetaDataField.Diff.disabled,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="running",
                kind=MetaData.Type.UINT,
                description="Running jobs",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="queued",
                kind=MetaData.Type.UINT,
                description="Queued jobs",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxRunning",
                kind=MetaData.Type.UINT,
                description="Maximum number of jobs that can run simultaneously",
                readonly=True,
                default=0,
            )
        )
        self.baseType = 'JobQueueStat'
        self.service_type = self.baseType
        self.allTypes = ['JobQueueStat']
        self.leaf_entity = False
        self.resolve_field_name = 'name'
        self.add_to_cluster = False
        self.allow_commit = False

