from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ResourcePool(Entity):
    class DNSZoneGeneration(Enum):
        BOTH = auto()
        FORWARD = auto()
        REVERSE = auto()
        NEITHER = auto()

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
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes who share the resources",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="configurationOverlay",
                kind=MetaData.Type.RESOLVE,
                description="Configuration overlay which defines the nodes that share the resources",
                instance='ConfigurationOverlay',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.FLOAT,
                description="Distribution priorities for the nodes",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="hostname",
                kind=MetaData.Type.STRING,
                description="Hostname all IP resources will point to",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="resources",
                kind=MetaData.Type.ENTITY,
                description="Resources to be divided among the given nodes",
                instance='BasicResource',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="waitTime",
                kind=MetaData.Type.UINT,
                description="How long to wait after a node goes down before migrating it's resources",
                default=5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disabled the entire resource pool",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="generateDNSZone",
                kind=MetaData.Type.ENUM,
                description="Specify which DNS zones should be written",
                options=[
                    self.DNSZoneGeneration.BOTH,
                    self.DNSZoneGeneration.FORWARD,
                    self.DNSZoneGeneration.REVERSE,
                    self.DNSZoneGeneration.NEITHER,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.DNSZoneGeneration,
                default=self.DNSZoneGeneration.BOTH,
            )
        )
        self.baseType = 'ResourcePool'
        self.service_type = self.baseType
        self.allTypes = ['ResourcePool']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

