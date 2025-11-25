from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class DnsRole(Role):
    """
    Dns role
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
        self.meta.add(
            MetaDataField(
                name="allowQuery",
                kind=MetaData.Type.STRING,
                description="List of additional free hosts to allow queries from",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="List of additional key=value pairs to add to the options",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxCacheSize",
                kind=MetaData.Type.UINT,
                description="Maximum cache size",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cleaningInterval",
                kind=MetaData.Type.UINT,
                description="Cleaning cache interval",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxCacheTTL",
                kind=MetaData.Type.UINT,
                description="Maximal cache TTL",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxNegativeCacheTTL",
                kind=MetaData.Type.UINT,
                description="Maximal cache negative response TTL",
                default=0,
            )
        )
        self.baseType = 'Role'
        self.childType = 'DnsRole'
        self.service_type = self.baseType
        self.allTypes = ['DnsRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

