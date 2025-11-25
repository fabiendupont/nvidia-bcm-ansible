from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FSxInstance(Entity):
    class ManagementType(Enum):
        UserManaged = auto()
        OnDemand = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="fsxId",
                kind=MetaData.Type.STRING,
                description="AWS assigned unique identifier",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Non-unique identifier",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="owner",
                kind=MetaData.Type.STRING,
                description="Owner of the FSx instance",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sharedWith",
                kind=MetaData.Type.STRING,
                description="Other cmjob users that can use this instance for jobs.",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="vpcId",
                kind=MetaData.Type.STRING,
                description="The VPC in which it exists",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="region",
                kind=MetaData.Type.STRING,
                description="The AWS region where the instance was created",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="capacity",
                kind=MetaData.Type.UINT,
                description="Instance capacity. Should be at least 3600 GiB.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.STRING,
                description="AWS reported status of the instance",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="hostname",
                kind=MetaData.Type.STRING,
                description="Hostname of the FSx, is internal to the VPC",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="management",
                kind=MetaData.Type.ENUM,
                description="Instance management type",
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
        self.baseType = 'FSxInstance'
        self.service_type = self.baseType
        self.allTypes = ['FSxInstance']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

