from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexpression import MonitoringExpression


class MonitoringGroupedExpression(MonitoringExpression):
    class Operator(Enum):
        OR = auto()
        AND = auto()

    def __init__(self):
        super().__init__()
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
        self.meta.add(
            MetaDataField(
                name="allowMissing",
                kind=MetaData.Type.BOOL,
                description="Allow missing sub expressions",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="expressions",
                kind=MetaData.Type.ENTITY,
                description="Expressions",
                instance='MonitoringCompareExpression',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringExpression'
        self.childType = 'MonitoringGroupedExpression'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringGroupedExpression', 'MonitoringExpression']
        self.top_level = False
        self.leaf_entity = True

