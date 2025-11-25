from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.nodehierarchyruleselection import NodeHierarchyRuleSelection


class NodeHierarchyRuleNodeGroupSelection(NodeHierarchyRuleSelection):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nodegroups",
                kind=MetaData.Type.RESOLVE,
                description="List of nodegroups",
                instance='NodeGroup',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'NodeHierarchyRuleSelection'
        self.childType = 'NodeHierarchyRuleNodeGroupSelection'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyRuleNodeGroupSelection', 'NodeHierarchyRuleSelection']
        self.top_level = False
        self.leaf_entity = True

