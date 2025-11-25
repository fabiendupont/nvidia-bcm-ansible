from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.wlmsubmitrole import WlmSubmitRole


class PbsProSubmitRole(WlmSubmitRole):
    """
    PbsPro submit role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="pbsProWlmClusters",
                kind=MetaData.Type.RESOLVE,
                description="List of PbsPro clusters which the role belongs to",
                instance='PbsProWlmCluster',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'PbsProSubmitRole'
        self.service_type = self.baseType
        self.allTypes = ['PbsProSubmitRole', 'WlmSubmitRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

