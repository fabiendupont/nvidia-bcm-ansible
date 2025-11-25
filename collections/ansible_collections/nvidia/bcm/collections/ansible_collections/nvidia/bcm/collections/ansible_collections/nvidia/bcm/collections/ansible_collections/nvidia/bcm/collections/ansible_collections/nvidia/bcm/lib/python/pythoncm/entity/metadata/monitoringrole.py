from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class MonitoringRole(Role):
    """
    Monitoring role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="numberOfBackups",
                kind=MetaData.Type.UINT,
                description="Minimum number of backups of the monitoring data",
                default=2,
            )
        )
        self.meta.add(
            MetaDataField(
                name="backupRing",
                kind=MetaData.Type.UINT,
                description="Only backup to nodes within the same ring",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maximumNumberOfNodes",
                kind=MetaData.Type.UINT,
                description="Maximum number of nodes the monitoring can handle, set to 0 for no limit",
                default=16384,
            )
        )
        self.meta.add(
            MetaDataField(
                name="delayAfterUp",
                kind=MetaData.Type.UINT,
                description="Delay after node becomes up before it can take over from other nodes",
                default=60,
            )
        )
        self.meta.add(
            MetaDataField(
                name="delayAfterDown",
                kind=MetaData.Type.UINT,
                description="Delay after node goes down before the workload will be offloaded to other nodes",
                default=600,
            )
        )
        self.meta.add(
            MetaDataField(
                name="backupOnShutdown",
                kind=MetaData.Type.BOOL,
                description="Take a backup when the node is shutdown via RPC",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="backupOnReboot",
                kind=MetaData.Type.BOOL,
                description="Take a backup when the node is reboot via RPC",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="backupOnPowerOff",
                kind=MetaData.Type.BOOL,
                description="Take a backup when the node is power off via RPC",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="backupOnPowerReset",
                kind=MetaData.Type.BOOL,
                description="Take a backup when the node is powered reset via RPC",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="backupOnTerminate",
                kind=MetaData.Type.BOOL,
                description="Take a backup when the cloud node is terminated via RPC",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeFilters",
                kind=MetaData.Type.ENTITY,
                description="Filter nodes that can be monitored by this node, clear this list for automatic",
                instance='MonitoringExecutionFilter',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'MonitoringRole'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

