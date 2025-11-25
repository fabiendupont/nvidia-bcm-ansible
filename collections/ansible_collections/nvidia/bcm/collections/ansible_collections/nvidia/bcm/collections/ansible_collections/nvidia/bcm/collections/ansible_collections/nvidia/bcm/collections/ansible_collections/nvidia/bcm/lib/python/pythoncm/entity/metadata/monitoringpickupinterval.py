from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringPickupInterval(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="interval",
                kind=MetaData.Type.FLOAT,
                description="Interval on which the RPC will be done",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="times",
                kind=MetaData.Type.UINT,
                description="Number of times the RPC will be done with the interval",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.UINT,
                description="Priority of the current pickup interval",
                default=0,
            )
        )
        self.baseType = 'MonitoringPickupInterval'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringPickupInterval']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

