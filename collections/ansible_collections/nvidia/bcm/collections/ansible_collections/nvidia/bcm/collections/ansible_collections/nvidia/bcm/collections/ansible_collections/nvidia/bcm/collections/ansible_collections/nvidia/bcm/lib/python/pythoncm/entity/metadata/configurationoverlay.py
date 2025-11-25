from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ConfigurationOverlay(Entity):
    """
    Configuration overlay
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="allHeadNodes",
                kind=MetaData.Type.BOOL,
                description="All head nodes",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes belonging to this group",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="categories",
                kind=MetaData.Type.RESOLVE,
                description="List of categories belonging to this group",
                instance='Category',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="customizationFiles",
                kind=MetaData.Type.ENTITY,
                description="Config file customizations",
                instance='CustomizationFile',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="roles",
                kind=MetaData.Type.ENTITY,
                description="Assign the roles",
                instance='Role',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.INT,
                description="Priority of the roles, node roles have a 750 priority, and category roles 250, set to -1 disable the overlay",
                default=500,
            )
        )
        self.baseType = 'ConfigurationOverlay'
        self.service_type = self.baseType
        self.allTypes = ['ConfigurationOverlay']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

