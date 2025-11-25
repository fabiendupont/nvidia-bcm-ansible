from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class DeviceStatus(Entity):
    class Status(Enum):
        UP = auto()
        DOWN = auto()
        PENDING = auto()
        INSTALLING = auto()
        INSTALLER_FAILED = auto()
        INSTALLER_REBOOTING = auto()
        INSTALLER_CALLING_INIT = auto()
        INSTALLER_UNREACHABLE = auto()
        GOING_DOWN = auto()
        BOOTING = auto()
        UNDEFINED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_device_uuid",
                kind=MetaData.Type.UUID,
                description="Device",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.ENUM,
                description="Status determined by ping and report",
                options=[
                    self.Status.UP,
                    self.Status.DOWN,
                    self.Status.PENDING,
                    self.Status.INSTALLING,
                    self.Status.INSTALLER_FAILED,
                    self.Status.INSTALLER_REBOOTING,
                    self.Status.INSTALLER_CALLING_INIT,
                    self.Status.INSTALLER_UNREACHABLE,
                    self.Status.GOING_DOWN,
                    self.Status.BOOTING,
                    self.Status.UNDEFINED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Status,
                default=self.Status.UNDEFINED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="reportedStatus",
                kind=MetaData.Type.ENUM,
                description="Reported status",
                options=[
                    self.Status.UP,
                    self.Status.DOWN,
                    self.Status.PENDING,
                    self.Status.INSTALLING,
                    self.Status.INSTALLER_FAILED,
                    self.Status.INSTALLER_REBOOTING,
                    self.Status.INSTALLER_CALLING_INIT,
                    self.Status.INSTALLER_UNREACHABLE,
                    self.Status.GOING_DOWN,
                    self.Status.BOOTING,
                    self.Status.UNDEFINED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Status,
                default=self.Status.UNDEFINED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="reportedStatusTimestamp",
                kind=MetaData.Type.UINT,
                description="Reported status timestamp in steady clock epoch milliseconds",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="leak",
                kind=MetaData.Type.UINT,
                description="Leak",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="terminated",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="closed",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="muted",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="burning",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="unassigned",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="noPingMethod",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nullIdentifier",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="additionalCost",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="restartRequired",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="healthCheckFailed",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="healthCheckUnknown",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="provisioningFailed",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stateFlapping",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stateFlappingCheckTime",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pingable",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sshable",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="infoMessage",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="userMessage",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="toolMessage",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="restartRequiredReasons",
                kind=MetaData.Type.STRING,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="gracePeriod",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerResetOnUnreachableCount",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="failBeforeDown",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updateIndex",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updateDisplay",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hasClientDaemon",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowDataNodeFullInstall",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.baseType = 'DeviceStatus'
        self.service_type = self.baseType
        self.allTypes = ['DeviceStatus']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

