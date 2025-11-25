from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiPDUOutlet(Entity):
    class Status(Enum):
        ON = auto()
        OFF = auto()
        RESET = auto()
        UNKNOWN = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="outlet",
                kind=MetaData.Type.UINT,
                description="Outlet",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.ENUM,
                description="Status",
                options=[
                    self.Status.ON,
                    self.Status.OFF,
                    self.Status.RESET,
                    self.Status.UNKNOWN,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Status,
                default=self.Status.UNKNOWN,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_assiged_devices_uuids",
                kind=MetaData.Type.UUID,
                description="Assigned",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'GuiPDUOutlet'
        self.service_type = self.baseType
        self.allTypes = ['GuiPDUOutlet']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

