from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.nodehierarchyruleselection import NodeHierarchyRuleSelection


class NodeHierarchyRuleTypeSelection(NodeHierarchyRuleSelection):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="headNode",
                kind=MetaData.Type.BOOL,
                description="Head node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="physicalNode",
                kind=MetaData.Type.BOOL,
                description="Physical node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cloudNode",
                kind=MetaData.Type.BOOL,
                description="Cloud node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liteNode",
                kind=MetaData.Type.BOOL,
                description="Lite node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dpuNode",
                kind=MetaData.Type.BOOL,
                description="Lite node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="networkSwitch",
                kind=MetaData.Type.BOOL,
                description="Network switch",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rackSensor",
                kind=MetaData.Type.BOOL,
                description="Rack sensor",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerDistributionUnit",
                kind=MetaData.Type.BOOL,
                description="Power distribution unit",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerShelf",
                kind=MetaData.Type.BOOL,
                description="Power shelf",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="coolingDistributionUnit",
                kind=MetaData.Type.BOOL,
                description="Cooling distribution unit",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="genericDevice",
                kind=MetaData.Type.BOOL,
                description="Generic device",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="chassis",
                kind=MetaData.Type.BOOL,
                description="Chassis",
                default=False,
            )
        )
        self.baseType = 'NodeHierarchyRuleSelection'
        self.childType = 'NodeHierarchyRuleTypeSelection'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyRuleTypeSelection', 'NodeHierarchyRuleSelection']
        self.top_level = False
        self.leaf_entity = True

