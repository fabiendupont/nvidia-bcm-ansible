from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringTrigger(Entity):
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
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disable",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="severity",
                kind=MetaData.Type.UINT,
                description="Severity",
                default=10,
            )
        )
        self.meta.add(
            MetaDataField(
                name="markEntityAsFailed",
                kind=MetaData.Type.BOOL,
                description="Mark entity as failed",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="markEntityAsUnknown",
                kind=MetaData.Type.BOOL,
                description="Mark entity as unknown",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stateFlappingPeriod",
                kind=MetaData.Type.FLOAT,
                description="Time period to check for state flapping",
                default=300.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stateFlappingCount",
                kind=MetaData.Type.UINT,
                description="Number of times states need to change in the specified period before it is considered stateflapping",
                default=5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="expression",
                kind=MetaData.Type.ENTITY,
                description="Expression",
                instance='MonitoringExpression',
                init_instance='MonitoringCompareExpression',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enterActions",
                kind=MetaData.Type.RESOLVE,
                description="Actions to execute when the expression enters 'true' state",
                instance='MonitoringAction',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="duringActions",
                kind=MetaData.Type.RESOLVE,
                description="Actions to execute when the expression is and has been 'true'",
                instance='MonitoringAction',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="leaveActions",
                kind=MetaData.Type.RESOLVE,
                description="Actions to execute when the expression is was 'true' and no longer is",
                instance='MonitoringAction',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="stateFlappingActions",
                kind=MetaData.Type.RESOLVE,
                description="Actions to execute when the expression is state flapping",
                instance='MonitoringAction',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringTrigger'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringTrigger']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

