from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class FailoverRole(Role):
    """
    Failover role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="syncCmShared",
                kind=MetaData.Type.BOOL,
                description="Passive head node has a local copy of /cm/shared",
                default=False,
            )
        )
        self.baseType = 'Role'
        self.childType = 'FailoverRole'
        self.service_type = self.baseType
        self.allTypes = ['FailoverRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

