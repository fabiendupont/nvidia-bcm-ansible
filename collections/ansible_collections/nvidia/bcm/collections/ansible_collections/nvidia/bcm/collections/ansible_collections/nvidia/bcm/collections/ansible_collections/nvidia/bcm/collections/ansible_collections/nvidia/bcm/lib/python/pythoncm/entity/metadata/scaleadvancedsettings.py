from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ScaleAdvancedSettings(Entity):
    class ScaleNodeSelection(Enum):
        ABS = auto()
        UPTIME = auto()
        RANDOM = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="debug2",
                kind=MetaData.Type.BOOL,
                description="Print very low level debug messages to the log",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxThreads",
                kind=MetaData.Type.UINT,
                description="Maximum number of threads for sequential operations",
                default=16,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerOperationTimeout",
                kind=MetaData.Type.UINT,
                description="Power Operation Timeout (in seconds)",
                default=30,
            )
        )
        self.meta.add(
            MetaDataField(
                name="connectionRetryInterval",
                kind=MetaData.Type.UINT,
                description="Connection to CMDaemon retry interval (in seconds)",
                default=5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="logFile",
                kind=MetaData.Type.STRING,
                description="Path to cm-scale logs file",
                default="/var/log/cm-scale.log",
            )
        )
        self.meta.add(
            MetaDataField(
                name="pinQueues",
                kind=MetaData.Type.BOOL,
                description="Pin workload to its queue nodes",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mixLocations",
                kind=MetaData.Type.BOOL,
                description="Allow to map workload to different locations (for example, cloud and local)",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="failedNodeIsHealthy",
                kind=MetaData.Type.BOOL,
                description="Do not start a new node instead of a failed one",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="collectStatistics",
                kind=MetaData.Type.BOOL,
                description="Collect internal Auto Scaler statistics and push to the monitoring",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="azureDiskAccountNodes",
                kind=MetaData.Type.UINT,
                description="Number of nodes that can share the same Azure disk account",
                default=20,
            )
        )
        self.meta.add(
            MetaDataField(
                name="azureDiskImageName",
                kind=MetaData.Type.STRING,
                description="Image name for Azure disks",
                default="images",
            )
        )
        self.meta.add(
            MetaDataField(
                name="azureDiskContainerName",
                kind=MetaData.Type.STRING,
                description="Container name for Azure disks",
                default="vhds",
            )
        )
        self.meta.add(
            MetaDataField(
                name="azureDiskAccountPrefix",
                kind=MetaData.Type.STRING,
                description="Prefix for randomly generated Azure disk account names",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeSelection",
                kind=MetaData.Type.ENUM,
                description="Type of node selection used by Auto Scaler",
                options=[
                    self.ScaleNodeSelection.ABS,
                    self.ScaleNodeSelection.UPTIME,
                    self.ScaleNodeSelection.RANDOM,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.ScaleNodeSelection,
                default=self.ScaleNodeSelection.ABS,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeSelectionUptimePeriod",
                kind=MetaData.Type.UINT,
                description="Period of time in which Auto Scaler calculates total uptime for the nodes during selection",
                default=1209600,
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Additional parameters that will be passed to cm-scale daemon",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ScaleAdvancedSettings'
        self.service_type = self.baseType
        self.allTypes = ['ScaleAdvancedSettings']
        self.top_level = False
        self.leaf_entity = True

