from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class OSService(Entity):
    class Status(Enum):
        DOWN = auto()
        UP = auto()
        STOPPED = auto()
        FAILING = auto()
        UNKNOWN = auto()
        NOTFOUND = auto()
        NOTNEEDED = auto()
        SICK = auto()
        INTERNAL = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="osserviceConfig",
                kind=MetaData.Type.ENTITY,
                description="OSServiceConfig",
                instance='OSServiceConfig',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.ENUM,
                description="",
                options=[
                    self.Status.DOWN,
                    self.Status.UP,
                    self.Status.STOPPED,
                    self.Status.FAILING,
                    self.Status.UNKNOWN,
                    self.Status.NOTFOUND,
                    self.Status.NOTNEEDED,
                    self.Status.SICK,
                    self.Status.INTERNAL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Status,
                default=self.Status.UNKNOWN,
            )
        )
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
                name="isRealService",
                kind=MetaData.Type.BOOL,
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sicknessMessage",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.baseType = 'OSService'
        self.service_type = self.baseType
        self.allTypes = ['OSService']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

