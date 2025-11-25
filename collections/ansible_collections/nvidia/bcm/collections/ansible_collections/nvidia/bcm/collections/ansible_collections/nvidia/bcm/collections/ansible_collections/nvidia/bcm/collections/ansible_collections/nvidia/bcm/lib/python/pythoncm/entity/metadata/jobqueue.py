from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class JobQueue(Entity):
    """
    Job queues
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name of queue",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="wlmCluster",
                kind=MetaData.Type.RESOLVE,
                description="WlmCluster to which this node belongs",
                instance='WlmCluster',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="overlays",
                kind=MetaData.Type.RESOLVE,
                description="Configuration overlays which nodes will be added to the queue (Slurm partition)",
                instance='ConfigurationOverlay',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="categories",
                kind=MetaData.Type.RESOLVE,
                description="List of node categories which nodes will be added to the queue (Slurm partition)",
                instance='Category',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodegroups",
                kind=MetaData.Type.RESOLVE,
                description="List of managed nodegroups",
                instance='NodeGroup',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="computeNodes",
                kind=MetaData.Type.RESOLVE,
                description="List of compute nodes that will be added to the queue",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Additional parameters that will be passed to the WLM queue configuration",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'JobQueue'
        self.service_type = self.baseType
        self.allTypes = ['JobQueue']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

