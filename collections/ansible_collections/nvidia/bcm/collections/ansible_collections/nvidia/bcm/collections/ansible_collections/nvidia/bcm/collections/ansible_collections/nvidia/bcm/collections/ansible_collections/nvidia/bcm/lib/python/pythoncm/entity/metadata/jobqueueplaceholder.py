from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class JobQueuePlaceholder(Entity):
    """
    Job queue placeholders
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="queue",
                kind=MetaData.Type.STRING,
                description="Name of queue",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="baseNodeName",
                kind=MetaData.Type.STRING,
                description="Placeholder node base name",
                default="placeholder",
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxNodes",
                kind=MetaData.Type.UINT,
                description="Maximum number of nodes in queue",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="templateNode",
                kind=MetaData.Type.RESOLVE,
                description="Node that will be used as a placeholder",
                instance='Node',
                default=None,
            )
        )
        self.baseType = 'JobQueuePlaceholder'
        self.service_type = self.baseType
        self.allTypes = ['JobQueuePlaceholder']
        self.top_level = False
        self.leaf_entity = True

