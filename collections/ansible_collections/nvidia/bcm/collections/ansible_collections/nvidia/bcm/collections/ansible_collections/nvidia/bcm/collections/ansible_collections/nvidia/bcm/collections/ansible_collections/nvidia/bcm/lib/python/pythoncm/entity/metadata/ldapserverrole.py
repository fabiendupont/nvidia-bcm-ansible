from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class LdapServerRole(Role):
    """
    LDAP server role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nodegroups",
                kind=MetaData.Type.RESOLVE,
                description="List of node groups which can boot from this node",
                instance='NodeGroup',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="categories",
                kind=MetaData.Type.RESOLVE,
                description="List of categories which can boot from this node",
                instance='Category',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="racks",
                kind=MetaData.Type.RESOLVE,
                description="List of racks which can boot from this node",
                instance='Rack',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'LdapServerRole'
        self.service_type = self.baseType
        self.allTypes = ['LdapServerRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

