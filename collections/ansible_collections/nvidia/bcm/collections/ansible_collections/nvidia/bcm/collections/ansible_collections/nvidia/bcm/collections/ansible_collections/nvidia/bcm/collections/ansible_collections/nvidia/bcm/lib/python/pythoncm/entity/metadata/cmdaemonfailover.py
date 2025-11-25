from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CMDaemonFailover(Entity):
    """
    Head node failover settings
    """
    class IpTakeOverMethod(Enum):
        ARP = auto()
        SCRIPT = auto()
        CLOUD = auto()
        LOAD_BALANCER = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="secondaryHeadNode",
                kind=MetaData.Type.RESOLVE,
                description="Secondary/failover head node",
                instance='HeadNode',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="keepalive",
                kind=MetaData.Type.UINT,
                description="Interval between pings",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="warntime",
                kind=MetaData.Type.UINT,
                description="How quickly to issue a 'late' warning",
                default=5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="deadtime",
                kind=MetaData.Type.UINT,
                description="How quickly to decide that a node in a cluster is dead",
                default=10,
            )
        )
        self.meta.add(
            MetaDataField(
                name="initdead",
                kind=MetaData.Type.UINT,
                description="Time between starting failover and declaring a cluster node dead",
                default=30,
            )
        )
        self.meta.add(
            MetaDataField(
                name="quorumTime",
                kind=MetaData.Type.UINT,
                description="Time before deciding quorum ended in failure",
                default=60,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountScript",
                kind=MetaData.Type.STRING,
                description="Script that mounts the shared storage device when a node becomes the active headnode",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="unmountScript",
                kind=MetaData.Type.STRING,
                description="Script that unmounts the shared storage device when a node stoppes being the active headnode",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="failoverNetwork",
                kind=MetaData.Type.RESOLVE,
                description="Network for failover ping",
                instance='Network',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableAutomaticFailover",
                kind=MetaData.Type.BOOL,
                description="When automatic failover is disabled the passive headnode will not take over if it detects the active headnode is dead",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="preFailoverScript",
                kind=MetaData.Type.STRING,
                description="Prefailover script will be run on both headnodes before failover has begun",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="postFailoverScript",
                kind=MetaData.Type.STRING,
                description="Postfailover script will be run on both headnodes after failover has completed",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ipTakeOverMethod",
                kind=MetaData.Type.ENUM,
                description="The manner in which shared IP gets transferred",
                options=[
                    self.IpTakeOverMethod.ARP,
                    self.IpTakeOverMethod.SCRIPT,
                    self.IpTakeOverMethod.CLOUD,
                    self.IpTakeOverMethod.LOAD_BALANCER,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.IpTakeOverMethod,
                default=self.IpTakeOverMethod.ARP,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ipTakeOverScript",
                kind=MetaData.Type.STRING,
                description="IP take over script",
                default='',
            )
        )
        self.baseType = 'CMDaemonFailover'
        self.service_type = self.baseType
        self.allTypes = ['CMDaemonFailover']
        self.top_level = False
        self.leaf_entity = True

