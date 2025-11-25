from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerScript(MonitoringDataProducer):
    class Format(Enum):
        AUTO = auto()
        TEXT = auto()
        JSON = auto()
        YAML = auto()
        XML = auto()
        MSGPACK = auto()
        PROTO_BUFFERS = auto()
        CBOR = auto()
        UBJSON = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="script",
                kind=MetaData.Type.STRING,
                description="Script",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.FLOAT,
                description="Script timeout",
                default=5.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="arguments",
                kind=MetaData.Type.STRING,
                description="Additional arguments to pass to the script",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="format",
                kind=MetaData.Type.ENUM,
                description="Expected output format",
                options=[
                    self.Format.AUTO,
                    self.Format.TEXT,
                    self.Format.JSON,
                    self.Format.YAML,
                    self.Format.MSGPACK,
                    self.Format.CBOR,
                    self.Format.UBJSON,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Format,
                default=self.Format.AUTO,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerScript'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerScript', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

