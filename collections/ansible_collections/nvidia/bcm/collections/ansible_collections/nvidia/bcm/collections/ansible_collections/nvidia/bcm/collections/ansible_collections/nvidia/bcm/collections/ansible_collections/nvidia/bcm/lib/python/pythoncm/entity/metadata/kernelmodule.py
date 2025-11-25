from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KernelModule(Entity):
    """
    Kernel module
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="The name of the kernel module.",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="parameters",
                kind=MetaData.Type.STRING,
                description="Options to be passed to the module.",
                default='',
            )
        )
        self.baseType = 'KernelModule'
        self.service_type = self.baseType
        self.allTypes = ['KernelModule']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

