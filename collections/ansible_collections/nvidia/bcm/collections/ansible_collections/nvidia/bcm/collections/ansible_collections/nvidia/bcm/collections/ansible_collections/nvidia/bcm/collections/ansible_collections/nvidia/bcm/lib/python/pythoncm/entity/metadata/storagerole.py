from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class StorageRole(Role):
    """
    Storage role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nfsThreads",
                kind=MetaData.Type.UINT,
                description="Number of nfs threads (0 for don't touch the current config file value)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableNFS1",
                kind=MetaData.Type.BOOL,
                description="Disable NFS1, NFS threads needs to bet set",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableNFS2",
                kind=MetaData.Type.BOOL,
                description="Disable NFS2, NFS threads needs to bet set",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableNFS3",
                kind=MetaData.Type.BOOL,
                description="Disable NFS3, NFS threads needs to bet set",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableNFS4",
                kind=MetaData.Type.BOOL,
                description="Disable NFS4, NFS threads needs to bet set",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nfs4grace",
                kind=MetaData.Type.UINT,
                description="NFS4 grace period (0 for don't touch the current config file value)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="statdPort",
                kind=MetaData.Type.UINT,
                description="Stat daemon port (0 for don't touch the current config file value)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="statdOutgoingPort",
                kind=MetaData.Type.UINT,
                description="Stat daemon outgoing port (0 for don't touch the current config file value)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountdPort",
                kind=MetaData.Type.UINT,
                description="Mount daemon port (0 for don't touch the current config file value)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rquotadPort",
                kind=MetaData.Type.UINT,
                description="Rquota daemon port (0 for don't touch the current config file value)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="lockdTcpPort",
                kind=MetaData.Type.UINT,
                description="Lock daemon TCP port (0 for don't touch the current config file value)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="lockdUdpPort",
                kind=MetaData.Type.UINT,
                description="Lock daemon UDP port (0 for don't touch the current config file value)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rdmaPort",
                kind=MetaData.Type.UINT,
                description="RDMA port (0 for don't touch the current config file value)",
                default=0,
            )
        )
        self.baseType = 'Role'
        self.childType = 'StorageRole'
        self.service_type = self.baseType
        self.allTypes = ['StorageRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

