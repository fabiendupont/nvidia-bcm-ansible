from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SlurmBlockTopologySettings(Entity):
    """
    Slurm Block topology plugin settings
    """
    class BlockEntityType(Enum):
        RACK = auto()
        NODEGROUP = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="blockSizes",
                kind=MetaData.Type.INT,
                description="List of the planning base block size, alongside any higher-level block sizes that would be enforced by topology/block plugin",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="blockEntity",
                kind=MetaData.Type.ENUM,
                description="What BCM entity represents a block",
                options=[
                    self.BlockEntityType.RACK,
                    self.BlockEntityType.NODEGROUP,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.BlockEntityType,
                default=self.BlockEntityType.RACK,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowedRacks",
                kind=MetaData.Type.RESOLVE,
                description="List of racks that will be used as blocks (if empty then all racks will be used)",
                instance='Rack',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowedNodeGroups",
                kind=MetaData.Type.RESOLVE,
                description="List of nodegroups that will be used as blocks (if empty then all nodegroups will be used)",
                instance='NodeGroup',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'SlurmBlockTopologySettings'
        self.service_type = self.baseType
        self.allTypes = ['SlurmBlockTopologySettings']
        self.top_level = False
        self.leaf_entity = True

