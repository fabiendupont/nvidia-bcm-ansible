from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.scaleresourceprovider import ScaleResourceProvider


class ScaleStaticNodesProvider(ScaleResourceProvider):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of managed nodes",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodegroups",
                kind=MetaData.Type.RESOLVE,
                description="List of managed nodegroups",
                instance='NodeGroup',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ScaleResourceProvider'
        self.childType = 'ScaleStaticNodesProvider'
        self.service_type = self.baseType
        self.allTypes = ['ScaleStaticNodesProvider', 'ScaleResourceProvider']
        self.top_level = False
        self.leaf_entity = True

