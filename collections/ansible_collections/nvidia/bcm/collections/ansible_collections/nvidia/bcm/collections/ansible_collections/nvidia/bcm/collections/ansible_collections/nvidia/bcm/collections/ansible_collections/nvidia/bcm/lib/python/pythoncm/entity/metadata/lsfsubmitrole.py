from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.wlmsubmitrole import WlmSubmitRole


class LSFSubmitRole(WlmSubmitRole):
    """
    LSF submit role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="lsfWlmClusters",
                kind=MetaData.Type.RESOLVE,
                description="List of LSF clusters which the role belongs to",
                instance='LSFWlmCluster',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="hostType",
                kind=MetaData.Type.STRING,
                description="Host type (possible values are defined in lsf.shared)",
                default="LINUX",
            )
        )
        self.baseType = 'Role'
        self.childType = 'LSFSubmitRole'
        self.service_type = self.baseType
        self.allTypes = ['LSFSubmitRole', 'WlmSubmitRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

