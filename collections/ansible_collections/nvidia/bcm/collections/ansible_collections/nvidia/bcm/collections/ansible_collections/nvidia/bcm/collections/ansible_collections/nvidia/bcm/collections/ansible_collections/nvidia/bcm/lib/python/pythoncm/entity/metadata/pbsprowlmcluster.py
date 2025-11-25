from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.wlmcluster import WlmCluster


class PbsProWlmCluster(WlmCluster):
    class PbsProSubType(Enum):
        PBSPRO = auto()
        OPENPBS = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.STRING,
                description="Major PBS Pro version",
                options=[
                    '20',
                    '21',
                    '22',
                    '22.05',
                    '23.06',
                    '24',
                    '25',
                ],
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="placeholders",
                kind=MetaData.Type.ENTITY,
                description="Job queue node placeholders mode",
                instance='JobQueuePlaceholder',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="cgroups",
                kind=MetaData.Type.ENTITY,
                description="Submode containing PBS Pro related cgroups settings",
                instance='PbsProCgroupsSettings',
                init_instance='PbsProCgroupsSettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pelogs",
                kind=MetaData.Type.ENTITY,
                description="Submode containing a list of PBS Pro related prolog and epilog (pelog) hook settings",
                instance='PbsPelog',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableJobHistory",
                kind=MetaData.Type.BOOL,
                description="Keep all job attribute information in PBS Pro",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobHistoryDuration",
                kind=MetaData.Type.STRING,
                description="Specifies the length of time that PBS will keep each job's history",
                regex_check=r"^([0-9]+:)+[0-9]+$",
                default="00:30:00",
            )
        )
        self.meta.add(
            MetaDataField(
                name="prefix",
                kind=MetaData.Type.STRING,
                description="PBS Pro installation directory",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="spool",
                kind=MetaData.Type.STRING,
                description="PBS Pro server spool directory",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="subType",
                kind=MetaData.Type.ENUM,
                description="PBS Pro subtype",
                options=[
                    self.PbsProSubType.PBSPRO,
                    self.PbsProSubType.OPENPBS,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.PbsProSubType,
                default=self.PbsProSubType.PBSPRO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="flatUid",
                kind=MetaData.Type.BOOL,
                description="Specifies whether a username at the submission host must be the same as the one at the server host",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxRunning",
                kind=MetaData.Type.UINT,
                description="Maximum number of jobs allowed to run at any given time (0 is the same as infinite)",
                default=0,
            )
        )
        self.baseType = 'WlmCluster'
        self.childType = 'PbsProWlmCluster'
        self.service_type = self.baseType
        self.allTypes = ['PbsProWlmCluster', 'WlmCluster']
        self.top_level = True
        self.leaf_entity = True

