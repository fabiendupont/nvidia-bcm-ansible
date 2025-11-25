from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProvisioningNodeStatus(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Provisioning node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_image_uuids",
                kind=MetaData.Type.UUID,
                description="Software images",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_category_uuids",
                kind=MetaData.Type.UUID,
                description="Categories",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_nodegroup_uuids",
                kind=MetaData.Type.UUID,
                description="Node groups",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_rack_uuids",
                kind=MetaData.Type.UUID,
                description="Racks",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="slotsCapacity",
                kind=MetaData.Type.UINT,
                description="Number of provisioning requests this node can handle in parallel.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="slotsUsed",
                kind=MetaData.Type.UINT,
                description="Number of provisioning requests currently being handled by this node.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="drained",
                kind=MetaData.Type.BOOL,
                description="Drained and not available for future request",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="upToDate",
                kind=MetaData.Type.BOOL,
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ProvisioningNodeStatus'
        self.service_type = self.baseType
        self.allTypes = ['ProvisioningNodeStatus']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

