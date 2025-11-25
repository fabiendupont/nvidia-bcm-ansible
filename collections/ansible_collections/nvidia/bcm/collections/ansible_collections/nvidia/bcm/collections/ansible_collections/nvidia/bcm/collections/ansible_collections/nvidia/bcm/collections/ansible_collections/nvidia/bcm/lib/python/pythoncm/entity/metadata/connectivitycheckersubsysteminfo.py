from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.subsysteminfo import SubSystemInfo


class ConnectivityCheckerSubSystemInfo(SubSystemInfo):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="stopped",
                kind=MetaData.Type.UINT,
                description="Stopped",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updateCallback",
                kind=MetaData.Type.UINT,
                description="Update callback defined",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="changeCallback",
                kind=MetaData.Type.UINT,
                description="Change callback defined",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ttl",
                kind=MetaData.Type.UINT,
                description="ttl",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="idOffset",
                kind=MetaData.Type.UINT,
                description="Ping ID offset",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="interval",
                kind=MetaData.Type.UINT,
                description="Interval",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.UINT,
                description="Timeout",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sequence",
                kind=MetaData.Type.UINT,
                description="Sequence ID",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="activeSequences",
                kind=MetaData.Type.UINT,
                description="Active ping sequences still being waited for",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="activeNodeSequences",
                kind=MetaData.Type.UINT,
                description="Number of nodes in active ping sequences still being waited for",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.UINT,
                description="Nodes being pinged",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeSequences",
                kind=MetaData.Type.UINT,
                description="Number of pings nodes are waiting for",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updates",
                kind=MetaData.Type.UINT,
                description="Total number of handled updates",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="changes",
                kind=MetaData.Type.UINT,
                description="Total number of handled changes",
                default=0,
            )
        )
        self.baseType = 'SubSystemInfo'
        self.childType = 'ConnectivityCheckerSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['ConnectivityCheckerSubSystemInfo', 'SubSystemInfo']
        self.top_level = False
        self.leaf_entity = True

