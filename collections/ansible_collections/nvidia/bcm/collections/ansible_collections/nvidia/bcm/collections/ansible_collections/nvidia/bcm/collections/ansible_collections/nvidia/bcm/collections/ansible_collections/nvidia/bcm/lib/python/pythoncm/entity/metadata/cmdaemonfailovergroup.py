from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CMDaemonFailoverGroup(Entity):
    """
    Failover group
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
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes belonging to this group",
                instance='ComputeNode',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="alsoTakeOverAfterGraciousShutdown",
                kind=MetaData.Type.BOOL,
                description="Also perform automatic failover if the active group member was gracefully shut down",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableAutomaticFailover",
                kind=MetaData.Type.BOOL,
                description="When automatic failover is disabled the no node in the group will not take over if the active node is dead",
                default=False,
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
                description="How quickly to decide that a node in a group is dead",
                default=10,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountScript",
                kind=MetaData.Type.STRING,
                description="Script that mounts the shared storage device when a node becomes the active head node",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="unmountScript",
                kind=MetaData.Type.STRING,
                description="Script that unmounts the shared storage device when a node stoppes being the active head node",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="preFailoverScript",
                kind=MetaData.Type.STRING,
                description="Prefailover script will be run on all nodes before failover has begun",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="postFailoverScript",
                kind=MetaData.Type.STRING,
                description="Postfailover script will be run on all nodes after failover has completed",
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
                description="Shared IP transfer script",
                default='',
            )
        )
        self.baseType = 'CMDaemonFailoverGroup'
        self.service_type = self.baseType
        self.allTypes = ['CMDaemonFailoverGroup']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

