from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProvisioningStatus(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="provisioningRequestStatusList",
                kind=MetaData.Type.ENTITY,
                instance='ProvisioningRequestStatus',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="provisioningNodeStatusList",
                kind=MetaData.Type.ENTITY,
                instance='ProvisioningNodeStatus',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ProvisioningStatus'
        self.service_type = self.baseType
        self.allTypes = ['ProvisioningStatus']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

