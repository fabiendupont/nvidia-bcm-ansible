from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class WlmNodeResource(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Resource name (Example: gpu)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraName",
                kind=MetaData.Type.STRING,
                description="Additional name (example: tesla)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="amount",
                kind=MetaData.Type.UINT,
                description="Resource amount",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="unit",
                kind=MetaData.Type.BOOL,
                description="The unit the amount is expressed in",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_node_uuids",
                kind=MetaData.Type.UUID,
                description="Node",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_wlm_cluster_uuid",
                kind=MetaData.Type.UUID,
                description="WlmCluster",
                default=self.zero_uuid,
            )
        )
        self.baseType = 'WlmNodeResource'
        self.service_type = self.baseType
        self.allTypes = ['WlmNodeResource']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

