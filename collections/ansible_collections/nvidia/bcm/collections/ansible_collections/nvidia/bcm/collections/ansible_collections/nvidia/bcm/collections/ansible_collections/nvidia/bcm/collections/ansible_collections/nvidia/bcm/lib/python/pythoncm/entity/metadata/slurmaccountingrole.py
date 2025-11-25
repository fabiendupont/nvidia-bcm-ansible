from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class SlurmAccountingRole(Role):
    """
    Slurm accounting role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ha",
                kind=MetaData.Type.BOOL,
                description="Generate a high availability configuration",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="primary",
                kind=MetaData.Type.RESOLVE,
                description="Primary server where slurmdbd will run",
                instance='Node',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dbdPort",
                kind=MetaData.Type.UINT,
                description="The port number that the Slurm Database Daemon (slurmdbd) listens to for work",
                default=6819,
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageHost",
                kind=MetaData.Type.STRING,
                description="Defines the name of the host the MySQL database is running where slurmdbd is going to store the data",
                default="master",
            )
        )
        self.meta.add(
            MetaDataField(
                name="storagePort",
                kind=MetaData.Type.UINT,
                description="The port number that the Slurm Database Daemon (slurmdbd) communicates with the database",
                default=3306,
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageLoc",
                kind=MetaData.Type.STRING,
                description="The name of the database as the location where slurmdbd accounting records are written",
                default="slurm_acct_db",
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageUser",
                kind=MetaData.Type.STRING,
                description="Defines the name of the user to connect to the MySQL database with to store the job accounting data",
                default="slurm",
            )
        )
        self.meta.add(
            MetaDataField(
                name="slurmWlmClusters",
                kind=MetaData.Type.RESOLVE,
                description="List of Slurm clusters which can make use of this SlurmAccountingRole (slurmdbd)",
                instance='SlurmWlmCluster',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'SlurmAccountingRole'
        self.service_type = self.baseType
        self.allTypes = ['SlurmAccountingRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

