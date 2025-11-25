from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GPUSettings(Entity):
    """
    GPU settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Range of GPUs for which these settings apply",
                required=True,
                default='',
            )
        )
        self.baseType = 'GPUSettings'
        self.service_type = self.baseType
        self.allTypes = ['GPUSettings']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

