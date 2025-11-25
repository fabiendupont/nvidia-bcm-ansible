from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class WlmFairshareOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_wlm_cluster_uuid",
                kind=MetaData.Type.UUID,
                description="WlmCluster",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fairshareTree",
                kind=MetaData.Type.JSON,
                description="Accounting fairshare tree",
                default=None,
            )
        )
        self.baseType = 'WlmFairshareOverview'
        self.service_type = self.baseType
        self.allTypes = ['WlmFairshareOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

