from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class DrainAction(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="node",
                kind=MetaData.Type.RESOLVE,
                description="Node",
                instance='Node',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="actions",
                kind=MetaData.Type.RESOLVE,
                description="Actions to execute after the node has been drained",
                instance='MonitoringAction',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'DrainAction'
        self.service_type = self.baseType
        self.allTypes = ['DrainAction']
        self.top_level = True
        self.leaf_entity = True

