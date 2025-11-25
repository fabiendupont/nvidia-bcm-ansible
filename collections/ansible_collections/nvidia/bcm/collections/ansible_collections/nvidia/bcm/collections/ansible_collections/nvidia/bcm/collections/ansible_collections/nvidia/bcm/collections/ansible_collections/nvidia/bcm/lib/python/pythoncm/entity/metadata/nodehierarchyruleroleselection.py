from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.nodehierarchyruleselection import NodeHierarchyRuleSelection


class NodeHierarchyRuleRoleSelection(NodeHierarchyRuleSelection):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="edgeDirector",
                kind=MetaData.Type.BOOL,
                description="Edge director",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cloudDirector",
                kind=MetaData.Type.BOOL,
                description="Cloud director",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="boot",
                kind=MetaData.Type.BOOL,
                description="Boot",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="provisioning",
                kind=MetaData.Type.BOOL,
                description="Provisioning",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dns",
                kind=MetaData.Type.BOOL,
                description="DNS",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ldap",
                kind=MetaData.Type.BOOL,
                description="LDAP",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="monitoring",
                kind=MetaData.Type.BOOL,
                description="Monitoring",
                default=False,
            )
        )
        self.baseType = 'NodeHierarchyRuleSelection'
        self.childType = 'NodeHierarchyRuleRoleSelection'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyRuleRoleSelection', 'NodeHierarchyRuleSelection']
        self.top_level = False
        self.leaf_entity = True

