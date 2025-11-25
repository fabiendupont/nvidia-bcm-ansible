from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class GenericRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="services",
                kind=MetaData.Type.STRING,
                description="Services managed by this role",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="configuration",
                kind=MetaData.Type.ENTITY,
                description="Configurations",
                instance='GenericRoleConfiguration',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraEnvironment",
                kind=MetaData.Type.ENTITY,
                description="Additional environment to be passed to scripts",
                instance='GenericRoleEnvironment',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeListSnippets",
                kind=MetaData.Type.ENTITY,
                instance='ExcludeListSnippet',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="dataNode",
                kind=MetaData.Type.BOOL,
                description="If enabled the node will never do a FULL install without explicit user confirmation",
                default=False,
            )
        )
        self.baseType = 'Role'
        self.childType = 'GenericRole'
        self.service_type = self.baseType
        self.allTypes = ['GenericRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

