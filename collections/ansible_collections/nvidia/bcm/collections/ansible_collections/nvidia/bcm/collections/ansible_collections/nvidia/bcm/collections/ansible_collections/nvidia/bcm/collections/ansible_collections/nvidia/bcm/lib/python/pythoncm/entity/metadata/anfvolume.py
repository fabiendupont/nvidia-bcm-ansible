from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ANFVolume(Entity):
    class ManagementType(Enum):
        UserManaged = auto()
        OnDemand = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="id",
                kind=MetaData.Type.STRING,
                description="Unique identifier",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name of the ANF volume.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="owner",
                kind=MetaData.Type.STRING,
                description="Owner of the Azure NetApp pool and volume",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="resourceGroup",
                kind=MetaData.Type.STRING,
                description="The resource group where the volume was created",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="netAppAccount",
                kind=MetaData.Type.STRING,
                description="The NetApp account name where the volume was created",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="location",
                kind=MetaData.Type.STRING,
                description="The Azure location where the volume was created",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Volume size. Should be at least 4 TiB.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.STRING,
                description="Status of the volume",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountPath",
                kind=MetaData.Type.STRING,
                description="String containing IP and mount path of the volume",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="management",
                kind=MetaData.Type.ENUM,
                description="Volume management type",
                options=[
                    self.ManagementType.UserManaged,
                    self.ManagementType.OnDemand,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.ManagementType,
                default=self.ManagementType.UserManaged,
            )
        )
        self.meta.add(
            MetaDataField(
                name="creationTime",
                kind=MetaData.Type.STRING,
                description="Creation time",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sharedWith",
                kind=MetaData.Type.STRING,
                description="Other cmjob users that can use this volume for jobs.",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ANFVolume'
        self.service_type = self.baseType
        self.allTypes = ['ANFVolume']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

