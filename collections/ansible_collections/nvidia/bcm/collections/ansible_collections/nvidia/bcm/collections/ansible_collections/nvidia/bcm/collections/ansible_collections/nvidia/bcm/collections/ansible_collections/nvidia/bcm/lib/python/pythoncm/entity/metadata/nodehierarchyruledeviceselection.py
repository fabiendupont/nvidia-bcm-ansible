from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.nodehierarchyruleselection import NodeHierarchyRuleSelection


class NodeHierarchyRuleDeviceSelection(NodeHierarchyRuleSelection):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="devices",
                kind=MetaData.Type.RESOLVE,
                description="List of devices",
                instance='Device',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'NodeHierarchyRuleSelection'
        self.childType = 'NodeHierarchyRuleDeviceSelection'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyRuleDeviceSelection', 'NodeHierarchyRuleSelection']
        self.top_level = False
        self.leaf_entity = True

