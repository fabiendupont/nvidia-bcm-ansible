from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GpuStatusEntry(Entity):
    """
    GPU status
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="index",
                kind=MetaData.Type.UINT,
                description="GPU index for this status entry",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpu",
                kind=MetaData.Type.STRING,
                description="Name of the GPU",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="property",
                kind=MetaData.Type.STRING,
                description="Property name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="value",
                kind=MetaData.Type.STRING,
                description="Value of the property",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="supported",
                kind=MetaData.Type.STRING,
                description="List of supported values for this property",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'GpuStatusEntry'
        self.service_type = self.baseType
        self.allTypes = ['GpuStatusEntry']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

