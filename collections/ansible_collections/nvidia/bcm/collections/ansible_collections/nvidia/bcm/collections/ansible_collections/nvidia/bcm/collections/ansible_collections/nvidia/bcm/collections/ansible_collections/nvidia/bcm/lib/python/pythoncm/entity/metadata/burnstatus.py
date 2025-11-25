from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BurnStatus(Entity):
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
                name="startNewBurn",
                kind=MetaData.Type.BOOL,
                description="Starting new burn on next reboot",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="burning",
                kind=MetaData.Type.BOOL,
                description="Currently burning",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="information",
                kind=MetaData.Type.STRING,
                description="Information",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="configuration",
                kind=MetaData.Type.STRING,
                description="Configuration",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="error",
                kind=MetaData.Type.STRING,
                description="Error message.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="warnings",
                kind=MetaData.Type.UINT,
                description="Number of warnings which have occurred so far.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="phaseName",
                kind=MetaData.Type.STRING,
                description="Name of the current phase.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="phaseTime",
                kind=MetaData.Type.STRING,
                description="Time past since the current phase was started.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="burnComplete",
                kind=MetaData.Type.STRING,
                description="Set if the burn cycle has completed.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="burnFailed",
                kind=MetaData.Type.BOOL,
                description="Set if the burn cycle has failed.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="testStatusList",
                kind=MetaData.Type.ENTITY,
                instance='BurnTestStatus',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'BurnStatus'
        self.service_type = self.baseType
        self.allTypes = ['BurnStatus']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

