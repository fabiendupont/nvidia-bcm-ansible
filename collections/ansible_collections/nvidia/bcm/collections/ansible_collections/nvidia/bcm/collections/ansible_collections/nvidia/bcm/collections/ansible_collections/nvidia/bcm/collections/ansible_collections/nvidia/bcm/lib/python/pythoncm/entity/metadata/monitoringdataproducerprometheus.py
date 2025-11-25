from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerPrometheus(MonitoringDataProducer):
    class Method(Enum):
        POST = auto()
        GET = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="urls",
                kind=MetaData.Type.STRING,
                description="One or more URLs to try connect to",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="method",
                kind=MetaData.Type.ENUM,
                description="HTTP method to use",
                options=[
                    self.Method.POST,
                    self.Method.GET,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Method,
                default=self.Method.POST,
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.UINT,
                description="Http get timeout",
                default=5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="passEnvironment",
                kind=MetaData.Type.BOOL,
                description="Pass the entity environment to the script",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="username",
                kind=MetaData.Type.STRING,
                description="Username used in http call",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="password",
                kind=MetaData.Type.STRING,
                description="Password used in http call",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="https",
                kind=MetaData.Type.BOOL,
                description="https",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="caPath",
                kind=MetaData.Type.STRING,
                description="CA certificate path",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="privateKeyPath",
                kind=MetaData.Type.STRING,
                description="Private key path",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="certificatePath",
                kind=MetaData.Type.STRING,
                description="Certificate path",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="staleTracking",
                kind=MetaData.Type.BOOL,
                description="Enable automatic tracking of stale metrics",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="withCertificate",
                kind=MetaData.Type.BOOL,
                description="Pass the cmdaemon certificate to make the call",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeProducerJobName",
                kind=MetaData.Type.BOOL,
                description="Automatically include producer job name in Prometheus label",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeEntityName",
                kind=MetaData.Type.BOOL,
                description="Automatically include entity name in Prometheus label",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="discardMetrics",
                kind=MetaData.Type.STRING,
                description="List of exact or regex matches to discard",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerPrometheus'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerPrometheus', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

