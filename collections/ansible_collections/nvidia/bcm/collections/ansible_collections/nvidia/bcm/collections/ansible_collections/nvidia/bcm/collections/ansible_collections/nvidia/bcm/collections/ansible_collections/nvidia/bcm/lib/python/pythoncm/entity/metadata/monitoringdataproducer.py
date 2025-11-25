from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringDataProducer(Entity):
    class When(Enum):
        TIMED = auto()
        ONDEMAND = auto()
        OOB = auto()
        ONSTART = auto()

    class Access(Enum):
        PUBLIC = auto()
        PRIVATE = auto()
        INDIVIDUAL = auto()

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
                name="description",
                kind=MetaData.Type.STRING,
                description="Description",
                default='',
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
        self.meta.add(
            MetaDataField(
                name="when",
                kind=MetaData.Type.ENUM,
                description="When the producer should run",
                options=[
                    self.When.TIMED,
                    self.When.ONDEMAND,
                    self.When.OOB,
                    self.When.ONSTART,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.When,
                default=self.When.TIMED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="preJob",
                kind=MetaData.Type.BOOL,
                description="Run as pre job in prolog",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="postJob",
                kind=MetaData.Type.BOOL,
                description="Run as post job in epilog",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxAge",
                kind=MetaData.Type.FLOAT,
                description="Maximal age of historic data, 0 for infinite",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxSamples",
                kind=MetaData.Type.UINT,
                description="Maximal samples of historic data, 0 for infinite",
                default=4096,
            )
        )
        self.meta.add(
            MetaDataField(
                name="interval",
                kind=MetaData.Type.FLOAT,
                description="Sampling interval",
                default=120.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="offset",
                kind=MetaData.Type.FLOAT,
                description="Time offset for sampling interval",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="startupDelay",
                kind=MetaData.Type.FLOAT,
                description="Delay the first sampling the specified time after cmd starts",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="intervals",
                kind=MetaData.Type.FLOAT,
                description="Out of band sampling interval",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="gap",
                kind=MetaData.Type.UINT,
                description="Number of missed samples before we add a NaN",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fuzzyOffset",
                kind=MetaData.Type.FLOAT,
                description="Automatic fuzzy offset factor [0-1]. Multiplied by interval",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="introduceNaN",
                kind=MetaData.Type.BOOL,
                description="Introduce NaN if device goes up/down/up",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxMeasurables",
                kind=MetaData.Type.UINT,
                description="Maximal number of measurables the producer can introduce",
                default=512,
            )
        )
        self.meta.add(
            MetaDataField(
                name="automaticReinitialize",
                kind=MetaData.Type.BOOL,
                description="Automatic run --initialize when a new metric has been detected",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disabled",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableTriggers",
                kind=MetaData.Type.BOOL,
                description="Disable triggers from being evaluated",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableOnHighLoad",
                kind=MetaData.Type.BOOL,
                description="Disable when nodes are very busy",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeExecutionFilters",
                kind=MetaData.Type.ENTITY,
                description="Filter nodes which should run this data producer. If none are specified: execute on each node.",
                instance='MonitoringExecutionFilter',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="executionMultiplexers",
                kind=MetaData.Type.ENTITY,
                description="Execute the producer once for each entity which matches one of the criteria. If none are specified: only execute it for the node itself.",
                instance='MonitoringExecutionMultiplexer',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="consolidator",
                kind=MetaData.Type.RESOLVE,
                description="Consolidator configuration",
                instance='MonitoringConsolidator',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="suppressedByGoingDown",
                kind=MetaData.Type.BOOL,
                description="Suppress running action if device is going down",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="access",
                kind=MetaData.Type.ENUM,
                description="User access control",
                options=[
                    self.Access.PUBLIC,
                    self.Access.PRIVATE,
                    self.Access.INDIVIDUAL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Access,
                default=self.Access.PUBLIC,
            )
        )
        self.meta.add(
            MetaDataField(
                name="associatedUser",
                kind=MetaData.Type.STRING,
                description="User associated with this measurable",
                default='',
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducer']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

