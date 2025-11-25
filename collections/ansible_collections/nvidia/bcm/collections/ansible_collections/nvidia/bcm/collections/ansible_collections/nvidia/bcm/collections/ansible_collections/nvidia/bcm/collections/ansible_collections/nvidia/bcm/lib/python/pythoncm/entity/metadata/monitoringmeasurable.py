from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringMeasurable(Entity):
    class SourceType(Enum):
        ANY = auto()
        BRIGHT = auto()
        PROMETHEUS = auto()
        BOTH = auto()

    class Access(Enum):
        PUBLIC = auto()
        PRIVATE = auto()
        INDIVIDUAL = auto()
        INHERIT = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="producer",
                kind=MetaData.Type.RESOLVE,
                description="Monitoring data producer",
                instance='MonitoringDataProducer',
                default=None,
            )
        )
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
                name="parameter",
                kind=MetaData.Type.STRING,
                description="Parameter",
                default='',
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
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disable: do not process or save to disk",
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
                name="gap",
                kind=MetaData.Type.UINT,
                description="Number of missed samples before we add a NaN",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="introduceNaN",
                kind=MetaData.Type.BOOL,
                description="Introduce NaN if device goes up/down/up",
                default=False,
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
                name="typeClass",
                kind=MetaData.Type.STRING,
                description="Type class, slash(/) separated for levels",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sourceType",
                kind=MetaData.Type.ENUM,
                description="Source of the measurable",
                options=[
                    self.SourceType.ANY,
                    self.SourceType.BRIGHT,
                    self.SourceType.PROMETHEUS,
                    self.SourceType.BOTH,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.SourceType,
                default=self.SourceType.BRIGHT,
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
                    self.Access.INHERIT,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Access,
                default=self.Access.INHERIT,
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
        self.baseType = 'MonitoringMeasurable'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringMeasurable']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

