from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.blockingoperation import BlockingOperation


class BlockingProvisioningOperation(BlockingOperation):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="request_uuids",
                kind=MetaData.Type.UUID,
                description="Request UUIDs",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'BlockingOperation'
        self.childType = 'BlockingProvisioningOperation'
        self.service_type = self.baseType
        self.allTypes = ['BlockingProvisioningOperation', 'BlockingOperation']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

