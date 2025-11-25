from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class ProvisioningRole(Role):
    """
    Provisioning role
    """
    class AllImages(Enum):
        LOCALDISK = auto()
        SHAREDSTORAGE = auto()
        NOTALLIMAGES = auto()
        LOCALUNLESSSHARED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="maxProvisioningNodes",
                kind=MetaData.Type.UINT,
                description="Maximum number of nodes that can be provisioned in parallel",
                default=10,
            )
        )
        self.meta.add(
            MetaDataField(
                name="loadWeight",
                kind=MetaData.Type.FLOAT,
                description="Load weight factor, higher factor will reduce the virtual load on the node and make it be used less. Value will be set to 1 if defined lower as lower than 1.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="localImages",
                kind=MetaData.Type.RESOLVE,
                description="List of software images provided from local disk",
                instance='SoftwareImage',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeRevisionsOfLocalImages",
                kind=MetaData.Type.BOOL,
                description="Include revisions of local images",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sharedImages",
                kind=MetaData.Type.RESOLVE,
                description="List of software images provided from shared storage",
                instance='SoftwareImage',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="allImages",
                kind=MetaData.Type.ENUM,
                description="When set, the role will provide all available images. (The images property will then be ignored.)",
                options=[
                    self.AllImages.LOCALDISK,
                    self.AllImages.SHAREDSTORAGE,
                    self.AllImages.NOTALLIMAGES,
                    self.AllImages.LOCALUNLESSSHARED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.AllImages,
                default=self.AllImages.NOTALLIMAGES,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodegroups",
                kind=MetaData.Type.RESOLVE,
                description="List of node groups for which to provide images",
                instance='NodeGroup',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="categories",
                kind=MetaData.Type.RESOLVE,
                description="List of categories for which to provide images",
                instance='Category',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="racks",
                kind=MetaData.Type.RESOLVE,
                description="List of racks for which to provide images",
                instance='Rack',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="localProvisioning",
                kind=MetaData.Type.BOOL,
                description="Speeds up initial provisioning of cloud directors and cloud provisioning nodes. When enabled, if a software image is used as the rootfs of the provisioning node and is also to be used by that node to provision other cloud nodes, during the initial FULL install that image will be transferred only once to the provisioning node, instead of twice.",
                default=True,
            )
        )
        self.baseType = 'Role'
        self.childType = 'ProvisioningRole'
        self.service_type = self.baseType
        self.allTypes = ['ProvisioningRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

