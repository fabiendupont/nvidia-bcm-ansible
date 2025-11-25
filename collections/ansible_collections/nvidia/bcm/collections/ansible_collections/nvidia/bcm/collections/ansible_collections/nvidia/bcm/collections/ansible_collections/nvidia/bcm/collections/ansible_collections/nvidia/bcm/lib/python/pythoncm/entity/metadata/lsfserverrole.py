from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.lsfrole import LSFRole


class LSFServerRole(LSFRole):
    """
    LSF server role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="externalServer",
                kind=MetaData.Type.BOOL,
                description="LSF server daemons are running on some external machine",
                default=False,
            )
        )
        self.baseType = 'Role'
        self.childType = 'LSFServerRole'
        self.service_type = self.baseType
        self.allTypes = ['LSFServerRole', 'LSFRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

