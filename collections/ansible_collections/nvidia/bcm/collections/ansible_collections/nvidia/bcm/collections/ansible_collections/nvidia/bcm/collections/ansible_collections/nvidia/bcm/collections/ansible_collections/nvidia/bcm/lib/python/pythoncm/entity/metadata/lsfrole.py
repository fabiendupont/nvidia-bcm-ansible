from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class LSFRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="wlmCluster",
                kind=MetaData.Type.RESOLVE,
                description="WLM cluster link to this WLM role",
                instance='LSFWlmCluster',
                default=None,
            )
        )
        self.baseType = 'Role'
        self.childType = 'LSFRole'
        self.service_type = self.baseType
        self.allTypes = ['LSFRole', 'Role']
        self.leaf_entity = False

