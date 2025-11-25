from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SlurmTopologySettings(Entity):
    """
    Slurm Topology settings
    """
    class TopologyPluginType(Enum):
        NONE = auto()
        DEFAULT = auto()
        TREE = auto()
        BLOCK = auto()
        TORUS = auto()

    class TopologySourceType(Enum):
        NONE = auto()
        INTERNAL = auto()
        TOPOGRAPH = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="topologyPlugin",
                kind=MetaData.Type.ENUM,
                description="Slurm topology plugin",
                options=[
                    self.TopologyPluginType.NONE,
                    self.TopologyPluginType.DEFAULT,
                    self.TopologyPluginType.TREE,
                    self.TopologyPluginType.BLOCK,
                    self.TopologyPluginType.TORUS,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.TopologyPluginType,
                default=self.TopologyPluginType.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="topologySource",
                kind=MetaData.Type.ENUM,
                description="Source of information for topology construction",
                options=[
                    self.TopologySourceType.NONE,
                    self.TopologySourceType.INTERNAL,
                    self.TopologySourceType.TOPOGRAPH,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.TopologySourceType,
                default=self.TopologySourceType.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="params",
                kind=MetaData.Type.ENTITY,
                description="Topology parameters for Slurm",
                instance='SlurmTopologyParams',
                init_instance='SlurmTopologyParams',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="treeSettings",
                kind=MetaData.Type.ENTITY,
                description="Tree topology plugin settings",
                instance='SlurmTreeTopologySettings',
                init_instance='SlurmTreeTopologySettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="blockSettings",
                kind=MetaData.Type.ENTITY,
                description="Block topology plugin settings",
                instance='SlurmBlockTopologySettings',
                init_instance='SlurmBlockTopologySettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="topographSettings",
                kind=MetaData.Type.ENTITY,
                description="Topograph service integaration settings",
                instance='SlurmTopographSettings',
                init_instance='SlurmTopographSettings',
                create_instance=True,
                default=None,
            )
        )
        self.baseType = 'SlurmTopologySettings'
        self.service_type = self.baseType
        self.allTypes = ['SlurmTopologySettings']
        self.top_level = False
        self.leaf_entity = True

