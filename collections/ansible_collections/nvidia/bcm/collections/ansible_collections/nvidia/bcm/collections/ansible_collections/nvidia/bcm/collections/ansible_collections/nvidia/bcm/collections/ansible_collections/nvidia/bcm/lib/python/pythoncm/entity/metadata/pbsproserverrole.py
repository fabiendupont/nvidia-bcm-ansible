from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.pbsprorole import PbsProRole


class PbsProServerRole(PbsProRole):
    """
    PbsPro server role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="externalServer",
                kind=MetaData.Type.BOOL,
                description="PBS Pro server daemons are running on some external machine",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="commSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing pbs_comm settings",
                instance='PbsProCommSettings',
                init_instance='PbsProCommSettings',
                create_instance=True,
                default=None,
            )
        )
        self.baseType = 'Role'
        self.childType = 'PbsProServerRole'
        self.service_type = self.baseType
        self.allTypes = ['PbsProServerRole', 'PbsProRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

