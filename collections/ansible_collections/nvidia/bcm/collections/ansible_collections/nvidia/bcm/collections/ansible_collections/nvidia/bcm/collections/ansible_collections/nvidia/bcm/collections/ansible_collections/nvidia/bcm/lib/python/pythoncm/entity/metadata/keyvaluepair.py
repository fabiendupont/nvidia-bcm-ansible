from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KeyValuePair(Entity):
    class Predicate(Enum):
        Equals = auto()
        HasPrefix = auto()
        ContainsString = auto()
        ContainsRegex = auto()
        MatchesRegex = auto()

    class RCPResult(Enum):
        Ok = auto()
        ConnectionError = auto()
        SqlError = auto()
        IllegalOperation = auto()
        KeyTooLong = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="key",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="value",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="onlydaemon",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ispattern",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.INT,
                default=100,
            )
        )
        self.baseType = 'KeyValuePair'
        self.service_type = self.baseType
        self.allTypes = ['KeyValuePair']
        self.top_level = False
        self.leaf_entity = True

