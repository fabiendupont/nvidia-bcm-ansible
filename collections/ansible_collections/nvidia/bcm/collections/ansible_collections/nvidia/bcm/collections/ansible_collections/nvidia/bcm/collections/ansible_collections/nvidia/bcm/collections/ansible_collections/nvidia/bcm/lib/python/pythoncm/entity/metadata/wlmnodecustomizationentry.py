from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class WlmNodeCustomizationEntry(Entity):
    """
    Node customization entry in a workload manager
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="key",
                kind=MetaData.Type.STRING,
                description="Name of the key",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="value",
                kind=MetaData.Type.STRING,
                description="Value for the key",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                description="Add the key/value to workload menegment node configuration or not",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Administrator notes",
                default='',
            )
        )
        self.baseType = 'WlmNodeCustomizationEntry'
        self.service_type = self.baseType
        self.allTypes = ['WlmNodeCustomizationEntry']
        self.top_level = False
        self.leaf_entity = True

