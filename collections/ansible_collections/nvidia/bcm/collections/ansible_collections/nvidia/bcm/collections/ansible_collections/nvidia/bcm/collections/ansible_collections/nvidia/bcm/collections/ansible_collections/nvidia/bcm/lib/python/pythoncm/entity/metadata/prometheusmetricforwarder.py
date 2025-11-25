from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PrometheusMetricForwarder(Entity):
    class Method(Enum):
        POST = auto()
        GET = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="The name of the prometheus metric forwarder",
                required=True,
                default='',
            )
        )
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
        self.baseType = 'PrometheusMetricForwarder'
        self.service_type = self.baseType
        self.allTypes = ['PrometheusMetricForwarder']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

