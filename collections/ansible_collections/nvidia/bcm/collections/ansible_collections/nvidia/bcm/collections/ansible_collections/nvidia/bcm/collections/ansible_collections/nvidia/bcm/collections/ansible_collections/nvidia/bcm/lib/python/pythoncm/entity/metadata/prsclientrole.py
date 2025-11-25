from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class PRSClientRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="staticPowerUsage",
                kind=MetaData.Type.UINT,
                description="Static power usage",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="staticPowerUsageDown",
                kind=MetaData.Type.UINT,
                description="Static power usage",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minPowerLimitCPU",
                kind=MetaData.Type.UINT,
                description="Overwrite the hardware min power limit for the CPUs",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxPowerLimitCPU",
                kind=MetaData.Type.UINT,
                description="Overwrite the hardware max power limit for the CPUs",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minPowerLimitGPU",
                kind=MetaData.Type.UINT,
                description="Overwrite the hardware min power limit for the GPUs",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxPowerLimitGPU",
                kind=MetaData.Type.UINT,
                description="Overwrite the hardware max power limit for the GPUs",
                default=0,
            )
        )
        self.baseType = 'Role'
        self.childType = 'PRSClientRole'
        self.service_type = self.baseType
        self.allTypes = ['PRSClientRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

