from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionmultiplexer import MonitoringExecutionMultiplexer


class MonitoringResourceExecutionMultiplexer(MonitoringExecutionMultiplexer):
    class Operator(Enum):
        OR = auto()
        AND = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="resources",
                kind=MetaData.Type.STRING,
                description="Resources",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="op",
                kind=MetaData.Type.ENUM,
                description="Operator",
                options=[
                    self.Operator.OR,
                    self.Operator.AND,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Operator,
                default=self.Operator.OR,
            )
        )
        self.baseType = 'MonitoringExecutionMultiplexer'
        self.childType = 'MonitoringResourceExecutionMultiplexer'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringResourceExecutionMultiplexer', 'MonitoringExecutionMultiplexer']
        self.top_level = False
        self.leaf_entity = True

