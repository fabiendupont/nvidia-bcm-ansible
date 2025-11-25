from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.nodehierarchyruleselection import NodeHierarchyRuleSelection


class NodeHierarchyRuleCategorySelection(NodeHierarchyRuleSelection):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="categories",
                kind=MetaData.Type.RESOLVE,
                description="List of categories",
                instance='Category',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'NodeHierarchyRuleSelection'
        self.childType = 'NodeHierarchyRuleCategorySelection'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyRuleCategorySelection', 'NodeHierarchyRuleSelection']
        self.top_level = False
        self.leaf_entity = True

