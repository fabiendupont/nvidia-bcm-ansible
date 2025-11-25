from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexpression import MonitoringExpression


class MonitoringCompareExpression(MonitoringExpression):
    class Grouping(Enum):
        ANY = auto()
        ALL = auto()
        SUM = auto()
        MIN = auto()
        MAX = auto()
        AVG = auto()

    class Operator(Enum):
        EQ = auto()
        NE = auto()
        LT = auto()
        GT = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="entities",
                kind=MetaData.Type.STRING,
                description="Entities matching the regex, leave empty for all",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="measurables",
                kind=MetaData.Type.STRING,
                description="Measurables matching the regex, leave empty for all",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="parameters",
                kind=MetaData.Type.STRING,
                description="Parameters matching the regex, leave empty for all",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="op",
                kind=MetaData.Type.ENUM,
                description="Operator",
                options=[
                    self.Operator.EQ,
                    self.Operator.NE,
                    self.Operator.LT,
                    self.Operator.GT,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Operator,
                default=self.Operator.EQ,
            )
        )
        self.meta.add(
            MetaDataField(
                name="grouping",
                kind=MetaData.Type.ENUM,
                description="Method to group all matching entity measurable parameter",
                options=[
                    self.Grouping.ANY,
                    self.Grouping.ALL,
                    self.Grouping.SUM,
                    self.Grouping.MIN,
                    self.Grouping.MAX,
                    self.Grouping.AVG,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Grouping,
                default=self.Grouping.ANY,
            )
        )
        self.meta.add(
            MetaDataField(
                name="value",
                kind=MetaData.Type.STRING,
                description="Value",
                default="FAIL",
            )
        )
        self.meta.add(
            MetaDataField(
                name="useRaw",
                kind=MetaData.Type.BOOL,
                description="Use raw data instead of rate for cumulative metrics",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="code",
                kind=MetaData.Type.STRING,
                description="Lua code",
                default='',
            )
        )
        self.baseType = 'MonitoringExpression'
        self.childType = 'MonitoringCompareExpression'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringCompareExpression', 'MonitoringExpression']
        self.top_level = False
        self.leaf_entity = True

