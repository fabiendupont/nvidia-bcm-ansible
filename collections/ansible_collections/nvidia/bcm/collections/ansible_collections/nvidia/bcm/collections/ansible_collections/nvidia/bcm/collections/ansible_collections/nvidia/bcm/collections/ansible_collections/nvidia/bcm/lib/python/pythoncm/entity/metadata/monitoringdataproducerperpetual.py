from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerPerpetual(MonitoringDataProducer):
    class Format(Enum):
        AUTO = auto()
        JSON = auto()
        YAML = auto()
        MSGPACK = auto()
        PROTO_BUFFERS = auto()
        PROMETHEUS = auto()

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
                name="runInBash",
                kind=MetaData.Type.BOOL,
                description="Run the script in a bash session",
                default=False,
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
                    self.Format.JSON,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Format,
                default=self.Format.AUTO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="watch",
                kind=MetaData.Type.BOOL,
                description="Watch script for changes, and restart",
                default=False,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerPerpetual'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerPerpetual', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

