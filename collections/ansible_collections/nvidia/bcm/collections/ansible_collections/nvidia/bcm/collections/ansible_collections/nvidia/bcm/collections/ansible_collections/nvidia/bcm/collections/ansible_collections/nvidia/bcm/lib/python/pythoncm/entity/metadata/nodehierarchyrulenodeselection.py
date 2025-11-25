from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.nodehierarchyruleselection import NodeHierarchyRuleSelection


class NodeHierarchyRuleNodeSelection(NodeHierarchyRuleSelection):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'NodeHierarchyRuleSelection'
        self.childType = 'NodeHierarchyRuleNodeSelection'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyRuleNodeSelection', 'NodeHierarchyRuleSelection']
        self.top_level = False
        self.leaf_entity = True

