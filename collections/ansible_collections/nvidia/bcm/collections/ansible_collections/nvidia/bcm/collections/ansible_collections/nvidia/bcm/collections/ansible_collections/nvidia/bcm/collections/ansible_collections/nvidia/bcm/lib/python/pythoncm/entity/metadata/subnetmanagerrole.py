from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class SubnetManagerRole(Role):
    """
    Subnet manager role
    """
    class Interconnect(Enum):
        IB = auto()
        OMNI = auto()

    class IBMTU(Enum):
        MTU_L2_2K = auto()
        MTU_L2_4K = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="interconnect",
                kind=MetaData.Type.ENUM,
                description="Type of interconnect",
                options=[
                    self.Interconnect.IB,
                    self.Interconnect.OMNI,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Interconnect,
                default=self.Interconnect.IB,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ibl2mtu",
                kind=MetaData.Type.ENUM,
                description="IB L2 MTU Value",
                options=[
                    self.IBMTU.MTU_L2_2K,
                    self.IBMTU.MTU_L2_4K,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.IBMTU,
                default=self.IBMTU.MTU_L2_2K,
            )
        )
        self.baseType = 'Role'
        self.childType = 'SubnetManagerRole'
        self.service_type = self.baseType
        self.allTypes = ['SubnetManagerRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

