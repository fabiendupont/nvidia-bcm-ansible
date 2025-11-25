from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class ScaleServerRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="engines",
                kind=MetaData.Type.ENTITY,
                description="Submode containing workload engines settings",
                instance='ScaleEngine',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="resourceProviders",
                kind=MetaData.Type.ENTITY,
                description="List of resource providers",
                instance='ScaleResourceProvider',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="dryRun",
                kind=MetaData.Type.BOOL,
                description="Run in dry run mode",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="debug",
                kind=MetaData.Type.BOOL,
                description="Print debug messages to the log",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="runInterval",
                kind=MetaData.Type.UINT,
                description="Frequency of cm-scale decision making (in seconds)",
                default=120,
            )
        )
        self.meta.add(
            MetaDataField(
                name="advancedSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing advanced settings",
                instance='ScaleAdvancedSettings',
                init_instance='ScaleAdvancedSettings',
                create_instance=True,
                default=None,
            )
        )
        self.baseType = 'Role'
        self.childType = 'ScaleServerRole'
        self.service_type = self.baseType
        self.allTypes = ['ScaleServerRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

