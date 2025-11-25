from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.nodehierarchyruleselection import NodeHierarchyRuleSelection


class NodeHierarchyRuleCloudRegionSelection(NodeHierarchyRuleSelection):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="regions",
                kind=MetaData.Type.RESOLVE,
                description="List of regions",
                instance='CloudRegion',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'NodeHierarchyRuleSelection'
        self.childType = 'NodeHierarchyRuleCloudRegionSelection'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyRuleCloudRegionSelection', 'NodeHierarchyRuleSelection']
        self.top_level = False
        self.leaf_entity = True

