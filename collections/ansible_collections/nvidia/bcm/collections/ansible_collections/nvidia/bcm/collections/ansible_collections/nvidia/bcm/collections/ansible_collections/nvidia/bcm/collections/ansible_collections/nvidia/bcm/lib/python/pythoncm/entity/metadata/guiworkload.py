from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiWorkload(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Queue name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="scheduler",
                kind=MetaData.Type.STRING,
                description="Scheduler",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="slots",
                kind=MetaData.Type.STRING,
                description="Slots",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_node_uuids",
                kind=MetaData.Type.UUID,
                description="Node",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.STRING,
                description="Nodes",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="running",
                kind=MetaData.Type.UINT,
                description="Number of running jobs in this queue",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="queued",
                kind=MetaData.Type.UINT,
                description="Number of pending jobs in this queue",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="error",
                kind=MetaData.Type.UINT,
                description="Number of jobs ended in an error state",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="completed",
                kind=MetaData.Type.UINT,
                description="Number of completed jobs",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="averageDuration",
                kind=MetaData.Type.FLOAT,
                description="Average duration of jobs",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="estimatedDelay",
                kind=MetaData.Type.FLOAT,
                description="Estimated delay for a new job to start",
                default=0.0,
            )
        )
        self.baseType = 'GuiWorkload'
        self.service_type = self.baseType
        self.allTypes = ['GuiWorkload']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

