from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FirewallPolicy(Entity):
    class Policy(Enum):
        ACCEPT = auto()
        BLACKLIST = auto()
        CONTINUE = auto()
        DROP = auto()
        NFQUEUE = auto()
        NONE = auto()
        QUEUE = auto()
        REJECT = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="source",
                kind=MetaData.Type.STRING,
                description="Source",
                default="loc",
            )
        )
        self.meta.add(
            MetaDataField(
                name="dest",
                kind=MetaData.Type.STRING,
                description="Dest",
                default="net",
            )
        )
        self.meta.add(
            MetaDataField(
                name="policy",
                kind=MetaData.Type.ENUM,
                description="Policy",
                options=[
                    self.Policy.ACCEPT,
                    self.Policy.BLACKLIST,
                    self.Policy.CONTINUE,
                    self.Policy.DROP,
                    self.Policy.NFQUEUE,
                    self.Policy.NONE,
                    self.Policy.QUEUE,
                    self.Policy.REJECT,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Policy,
                default=self.Policy.ACCEPT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="log",
                kind=MetaData.Type.STRING,
                description="Log",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Options",
                default="",
            )
        )
        self.baseType = 'FirewallPolicy'
        self.service_type = self.baseType
        self.allTypes = ['FirewallPolicy']
        self.top_level = False
        self.leaf_entity = True

