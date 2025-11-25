from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BeeGFSLogSettings(Entity):
    """
    BeeGFS logging settings entry
    """
    class BeeGFSLogType(Enum):
        SYSLOG = auto()
        LOGFILE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="logType",
                kind=MetaData.Type.ENUM,
                description="Defines the logger type. This can either be 'syslog' to send log messages to the general system logger or 'logfile'",
                options=[
                    self.BeeGFSLogType.SYSLOG,
                    self.BeeGFSLogType.LOGFILE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.BeeGFSLogType,
                default=self.BeeGFSLogType.SYSLOG,
            )
        )
        self.meta.add(
            MetaDataField(
                name="level",
                kind=MetaData.Type.UINT,
                description="Log level",
                default=2,
            )
        )
        self.meta.add(
            MetaDataField(
                name="noDate",
                kind=MetaData.Type.BOOL,
                description="Do not show date along with time in log",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfLines",
                kind=MetaData.Type.UINT,
                description="Number of lines in log file, after which it will be rotated",
                default=50000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfRotatedFiles",
                kind=MetaData.Type.UINT,
                description="Number of old log files to keep",
                default=5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="file",
                kind=MetaData.Type.STRING,
                description="Path to the log file, empty means logs go to the journal",
                regex_check=r"^(/[^\s\0]+)?$",
                default="",
            )
        )
        self.baseType = 'BeeGFSLogSettings'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSLogSettings']
        self.top_level = False
        self.leaf_entity = True

