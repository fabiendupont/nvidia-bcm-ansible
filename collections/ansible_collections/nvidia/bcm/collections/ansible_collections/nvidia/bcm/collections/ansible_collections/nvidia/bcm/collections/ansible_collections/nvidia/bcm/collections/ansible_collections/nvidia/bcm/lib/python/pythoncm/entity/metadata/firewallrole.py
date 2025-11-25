from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class FirewallRole(Role):
    """
    Firewall role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="shorewall",
                kind=MetaData.Type.BOOL,
                description="Manage shorewall",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="openPorts",
                kind=MetaData.Type.ENTITY,
                description="The list of ports that will be opened on the node's firewall",
                instance='FirewallOpenPort',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="zones",
                kind=MetaData.Type.ENTITY,
                description="The list of extra zones that will be defined in the node's firewall",
                instance='FirewallZone',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="interfaces",
                kind=MetaData.Type.ENTITY,
                description="The list of extra interfaces that will be defined in the node's firewall",
                instance='FirewallInterface',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="policies",
                kind=MetaData.Type.ENTITY,
                description="The list of extra policies that will be defined in the node's firewall",
                instance='FirewallPolicy',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="routes",
                kind=MetaData.Type.ENTITY,
                description="The list of extra routes that will be defined in the node's firewall",
                instance='FirewallRoute',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'FirewallRole'
        self.service_type = self.baseType
        self.allTypes = ['FirewallRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

