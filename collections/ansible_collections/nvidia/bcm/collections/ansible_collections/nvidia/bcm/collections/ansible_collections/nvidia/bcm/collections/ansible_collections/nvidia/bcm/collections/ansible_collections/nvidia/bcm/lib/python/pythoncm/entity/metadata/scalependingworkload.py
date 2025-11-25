from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ScalePendingWorkload(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="workloadId",
                kind=MetaData.Type.STRING,
                description="Workload that waits for nodes",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of managed nodes",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ScalePendingWorkload'
        self.service_type = self.baseType
        self.allTypes = ['ScalePendingWorkload']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'workloadId'

