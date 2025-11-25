from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class EdgeSite(Entity):
    class CreateImage(Enum):
        SCRIPT = auto()
        NO = auto()
        YES = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="contact",
                kind=MetaData.Type.STRING,
                description="Names of contacts",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="adminEmail",
                kind=MetaData.Type.STRING,
                description="Administrator's email",
                function_check=MetaData.check_isEmail,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="address",
                kind=MetaData.Type.STRING,
                description="Address",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="city",
                kind=MetaData.Type.STRING,
                description="City",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="country",
                kind=MetaData.Type.STRING,
                description="Country",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeZoneSettings",
                kind=MetaData.Type.ENTITY,
                description="Time zone",
                instance='TimeZoneSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Notes",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes in this site",
                instance='ComputeNode',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="switches",
                kind=MetaData.Type.RESOLVE,
                description="List of switches in this site",
                instance='Switch',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="genericDevices",
                kind=MetaData.Type.RESOLVE,
                description="List of generic devices in this site",
                instance='GenericDevice',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerDistributionUnits",
                kind=MetaData.Type.RESOLVE,
                description="List of power distribution units in this site",
                instance='PowerDistributionUnit',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="racks",
                kind=MetaData.Type.RESOLVE,
                description="List of racks in this site",
                instance='Rack',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="secret",
                kind=MetaData.Type.STRING,
                description="Edge site secret",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="metaDataDeviceLabel",
                kind=MetaData.Type.STRING,
                description="Meta data device label which to mount in order get the meta data",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="metaDataUrl",
                kind=MetaData.Type.STRING,
                description="Meta data URL that contains information for edge directors",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="createISO",
                kind=MetaData.Type.ENUM,
                description="Edge site site ISO/script for USB",
                options=[
                    self.CreateImage.SCRIPT,
                    self.CreateImage.NO,
                    self.CreateImage.YES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.CreateImage,
                default=self.CreateImage.SCRIPT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="createIMG",
                kind=MetaData.Type.ENUM,
                description="Edge site site IMG/script for MMC",
                options=[
                    self.CreateImage.SCRIPT,
                    self.CreateImage.NO,
                    self.CreateImage.YES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.CreateImage,
                default=self.CreateImage.SCRIPT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeCMSharedOnMedia",
                kind=MetaData.Type.BOOL,
                description="Include /cm/shared on media to reduce the amount of rsync during edge director installation",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeImagesOnMedia",
                kind=MetaData.Type.BOOL,
                description="Include images on media to reduce the amount of rsync during edge director installation",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="preStageRequestID",
                kind=MetaData.Type.UUID,
                description="Pre-staging request ID",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="preStageRequestIDCreationTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Pre-staging request ID creation time",
                default=0,
            )
        )
        self.baseType = 'EdgeSite'
        self.service_type = self.baseType
        self.allTypes = ['EdgeSite']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

