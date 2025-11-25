from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KubeLabelSet(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Object name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="labels",
                kind=MetaData.Type.STRING,
                description="Node labels",
                regex_check=r"^[a-z0-9A-Z][a-z0-9A-Z/_.-]*=([a-z0-9A-Z][a-z0-9A-Z_.-]*)?$",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes belonging to this label set",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="categories",
                kind=MetaData.Type.RESOLVE,
                description="List of categories belonging to this label set",
                instance='Category',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="overlays",
                kind=MetaData.Type.RESOLVE,
                description="List of overlays belonging to this label set",
                instance='ConfigurationOverlay',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'KubeLabelSet'
        self.service_type = self.baseType
        self.allTypes = ['KubeLabelSet']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

