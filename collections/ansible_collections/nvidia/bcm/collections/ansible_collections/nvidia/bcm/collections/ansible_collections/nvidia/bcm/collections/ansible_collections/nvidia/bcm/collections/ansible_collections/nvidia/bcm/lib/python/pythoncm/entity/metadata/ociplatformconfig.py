from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class OCIPlatformConfig(Entity):
    class OptionalBool(Enum):
        DEFAULT = auto()
        NO = auto()
        YES = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="platformType",
                kind=MetaData.Type.STRING,
                description="The type of platform being configured.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="isSecureBootEnabled",
                kind=MetaData.Type.ENUM,
                description="Whether Secure Boot is enabled on the instance.",
                options=[
                    self.OptionalBool.DEFAULT,
                    self.OptionalBool.NO,
                    self.OptionalBool.YES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.OptionalBool,
                default=self.OptionalBool.DEFAULT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="isTrustedPlatformModuleEnabled",
                kind=MetaData.Type.ENUM,
                description="Whether the Trusted Platform Module (TPM) is enabled on the instance.",
                options=[
                    self.OptionalBool.DEFAULT,
                    self.OptionalBool.NO,
                    self.OptionalBool.YES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.OptionalBool,
                default=self.OptionalBool.DEFAULT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="isMeasuredBootEnabled",
                kind=MetaData.Type.ENUM,
                description="Whether the Measured Boot feature is enabled on the instance.",
                options=[
                    self.OptionalBool.DEFAULT,
                    self.OptionalBool.NO,
                    self.OptionalBool.YES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.OptionalBool,
                default=self.OptionalBool.DEFAULT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="isMemoryEncryptionEnabled",
                kind=MetaData.Type.ENUM,
                description="Whether the instance is a confidential instance.",
                options=[
                    self.OptionalBool.DEFAULT,
                    self.OptionalBool.NO,
                    self.OptionalBool.YES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.OptionalBool,
                default=self.OptionalBool.DEFAULT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numaNodesPerSocket",
                kind=MetaData.Type.STRING,
                description="The number of NUMA nodes per socket (NPS).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="isSymmetricMultiThreadingEnabled",
                kind=MetaData.Type.ENUM,
                description="Whether symmetric multithreading is enabled on the instance. Symmetric multithreading is also called simultaneous multithreading (SMT) or Intel Hyper-Threading. Intel and AMD processors have two hardware execution threads per core (OCPU). SMT permits multiple independent threads of execution, to better use the resources and increase the efficiency of the CPU. When multithreading is disabled, only one thread is permitted to run on each core, which can provide higher or more predictable performance for some workloads.",
                options=[
                    self.OptionalBool.DEFAULT,
                    self.OptionalBool.NO,
                    self.OptionalBool.YES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.OptionalBool,
                default=self.OptionalBool.DEFAULT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="isAccessControlServiceEnabled",
                kind=MetaData.Type.ENUM,
                description="Whether the Access Control Service is enabled on the instance. When enabled, the platform can enforce PCIe device isolation, required for VFIO device pass-through.",
                options=[
                    self.OptionalBool.DEFAULT,
                    self.OptionalBool.NO,
                    self.OptionalBool.YES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.OptionalBool,
                default=self.OptionalBool.DEFAULT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="areVirtualInstructionsEnabled",
                kind=MetaData.Type.ENUM,
                description="Whether virtualization instructions are available. For example, Secure Virtual Machine for AMD shapes or VT-x for Intel shapes.",
                options=[
                    self.OptionalBool.DEFAULT,
                    self.OptionalBool.NO,
                    self.OptionalBool.YES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.OptionalBool,
                default=self.OptionalBool.DEFAULT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="isInputOutputMemoryManagementUnitEnabled",
                kind=MetaData.Type.ENUM,
                description="Whether the input-output memory management unit is enabled.",
                options=[
                    self.OptionalBool.DEFAULT,
                    self.OptionalBool.NO,
                    self.OptionalBool.YES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.OptionalBool,
                default=self.OptionalBool.DEFAULT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="percentageOfCoresEnabled",
                kind=MetaData.Type.UINT,
                description="The percentage of cores enabled. Value must be a multiple of 25%. If the requested percentage results in a fractional number of cores, the system rounds up the number of cores across processors and provisions an instance with a whole number of cores. If the applications that you run on the instance use a core-based licensing model and need fewer cores than the full size of the shape, you can disable cores to reduce your licensing costs. The instance itself is billed for the full shape, regardless of whether all cores are enabled.",
                default=0,
            )
        )
        self.baseType = 'OCIPlatformConfig'
        self.service_type = self.baseType
        self.allTypes = ['OCIPlatformConfig']
        self.top_level = False
        self.leaf_entity = True

