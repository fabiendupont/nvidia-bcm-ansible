from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PRSDomain(Entity):
    class PowerBudgetModel(Enum):
        SCALAR = auto()

    class PowerDrawModel(Enum):
        LINEAR = auto()

    class GroupBy(Enum):
        ALL = auto()
        RACK = auto()
        ROW = auto()
        ROOM = auto()
        BUILDING = auto()
        LOCATION = auto()
        CIRCUIT = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerBudget",
                kind=MetaData.Type.UINT,
                description="Power budget",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerDrawFactor",
                kind=MetaData.Type.FLOAT,
                description="Power draw factor",
                default=1.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerDrawModel",
                kind=MetaData.Type.ENUM,
                description="Power draw model",
                options=[self.PowerDrawModel.LINEAR],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.PowerDrawModel,
                default=self.PowerDrawModel.LINEAR,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerBudgetModel",
                kind=MetaData.Type.ENUM,
                description="Power budget model",
                options=[self.PowerBudgetModel.SCALAR],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.PowerBudgetModel,
                default=self.PowerBudgetModel.SCALAR,
            )
        )
        self.meta.add(
            MetaDataField(
                name="groupBy",
                kind=MetaData.Type.ENUM,
                description="Create a domain per group",
                options=[
                    self.GroupBy.ALL,
                    self.GroupBy.RACK,
                    self.GroupBy.ROW,
                    self.GroupBy.ROOM,
                    self.GroupBy.BUILDING,
                    self.GroupBy.LOCATION,
                    self.GroupBy.CIRCUIT,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.GroupBy,
                default=self.GroupBy.ALL,
            )
        )
        self.meta.add(
            MetaDataField(
                name="autostart",
                kind=MetaData.Type.BOOL,
                description="Auto start domain on creation",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeNodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes to exclude from the domain",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeRacks",
                kind=MetaData.Type.RESOLVE,
                description="List of racks to exclude from the domain",
                instance='Rack',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'PRSDomain'
        self.service_type = self.baseType
        self.allTypes = ['PRSDomain']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

