from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CMDaemonBackgroundTask(Entity):
    class Status(Enum):
        PENDING = auto()
        RUNNING = auto()
        CANCELED = auto()
        FAILED = auto()
        DONE = auto()

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
                name="ref_entity_uuid",
                kind=MetaData.Type.UUID,
                description="Entity",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="updates",
                kind=MetaData.Type.STRING,
                description="Updates",
                readonly=True,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="exitCode",
                kind=MetaData.Type.INT,
                description="Exit code",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.ENUM,
                description="Status",
                options=[
                    self.Status.PENDING,
                    self.Status.RUNNING,
                    self.Status.CANCELED,
                    self.Status.FAILED,
                    self.Status.DONE,
                ],
                readonly=True,
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Status,
                default=self.Status.PENDING,
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.UINT,
                description="Start time",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="endTime",
                kind=MetaData.Type.UINT,
                description="End time",
                readonly=True,
                default=0,
            )
        )
        self.baseType = 'CMDaemonBackgroundTask'
        self.service_type = self.baseType
        self.allTypes = ['CMDaemonBackgroundTask']
        self.top_level = False
        self.leaf_entity = True

