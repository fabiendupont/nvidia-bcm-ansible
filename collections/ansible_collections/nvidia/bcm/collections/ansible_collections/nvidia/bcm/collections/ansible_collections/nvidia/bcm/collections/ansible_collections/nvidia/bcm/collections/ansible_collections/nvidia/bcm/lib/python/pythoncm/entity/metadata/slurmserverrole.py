from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.slurmrole import SlurmRole


class SlurmServerRole(SlurmRole):
    """
    Slurm server role
    """
    class SlurmctldStartPolicy(Enum):
        ALWAYS = auto()
        TAKEOVER = auto()
        ACTIVEONLY = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="externalServer",
                kind=MetaData.Type.BOOL,
                description="Slurm server daemons are running on some external machine",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="slurmctldStartPolicy",
                kind=MetaData.Type.ENUM,
                description="Determines when slurmctld must be running across slurm servernodes",
                options=[
                    self.SlurmctldStartPolicy.ALWAYS,
                    self.SlurmctldStartPolicy.TAKEOVER,
                    self.SlurmctldStartPolicy.ACTIVEONLY,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.SlurmctldStartPolicy,
                default=self.SlurmctldStartPolicy.ALWAYS,
            )
        )
        self.baseType = 'Role'
        self.childType = 'SlurmServerRole'
        self.service_type = self.baseType
        self.allTypes = ['SlurmServerRole', 'SlurmRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

