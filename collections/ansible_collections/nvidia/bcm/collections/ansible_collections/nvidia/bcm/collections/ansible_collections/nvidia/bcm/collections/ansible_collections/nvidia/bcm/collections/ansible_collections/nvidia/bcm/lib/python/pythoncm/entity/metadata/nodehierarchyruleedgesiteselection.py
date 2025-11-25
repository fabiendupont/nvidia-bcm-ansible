from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.nodehierarchyruleselection import NodeHierarchyRuleSelection


class NodeHierarchyRuleEdgeSiteSelection(NodeHierarchyRuleSelection):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="edgesites",
                kind=MetaData.Type.RESOLVE,
                description="List of edgesites",
                instance='EdgeSite',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'NodeHierarchyRuleSelection'
        self.childType = 'NodeHierarchyRuleEdgeSiteSelection'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyRuleEdgeSiteSelection', 'NodeHierarchyRuleSelection']
        self.top_level = False
        self.leaf_entity = True

