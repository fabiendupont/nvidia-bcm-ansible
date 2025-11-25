from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ChargeBackRequest(Entity):
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
                name="groupByUser",
                kind=MetaData.Type.BOOL,
                description="Group by user",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="groupByGroup",
                kind=MetaData.Type.BOOL,
                description="Group by group",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="groupByAccount",
                kind=MetaData.Type.BOOL,
                description="Group by account",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="groupByJobName",
                kind=MetaData.Type.BOOL,
                description="Group by job name",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="groupByJobId",
                kind=MetaData.Type.BOOL,
                description="Group by job ID",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="groupByAccountingInfo",
                kind=MetaData.Type.STRING,
                description="Group by accounting info",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="users",
                kind=MetaData.Type.STRING,
                description="Users",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="groups",
                kind=MetaData.Type.STRING,
                description="Users",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="accounts",
                kind=MetaData.Type.STRING,
                description="Accounts",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobNames",
                kind=MetaData.Type.STRING,
                description="Job names",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobIds",
                kind=MetaData.Type.STRING,
                description="Job IDs",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="accountingInfo",
                kind=MetaData.Type.JSON,
                description="Accounting info",
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="wlmClusters",
                kind=MetaData.Type.RESOLVE,
                description="List of wlm clusters which to include, empty for all",
                instance='WlmCluster',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="pricePerCPUSecond",
                kind=MetaData.Type.FLOAT,
                description="Price per CPU second",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pricePerCPUCoreSecond",
                kind=MetaData.Type.FLOAT,
                description="Price per CPU core second",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pricePerGPUSecond",
                kind=MetaData.Type.FLOAT,
                description="Price per GPU second",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pricePerMemoryByteSecond",
                kind=MetaData.Type.FLOAT,
                description="Price per memory byte-second",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pricePerSlotSecond",
                kind=MetaData.Type.FLOAT,
                description="Price per slot second",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pricePerWattSecond",
                kind=MetaData.Type.FLOAT,
                description="Price per Watt second",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="currency",
                kind=MetaData.Type.STRING,
                description="Currency",
                default="$",
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.STRING,
                description="Start time",
                regex_check=r"^[0-9]+|now(([-+][0-9]+)+([smhdwMy]))?(/[smhdwMy])?$",
                default="now/M",
            )
        )
        self.meta.add(
            MetaDataField(
                name="endTime",
                kind=MetaData.Type.STRING,
                description="End time",
                regex_check=r"^[0-9]+|now(([-+][0-9]+)+([smhdwMy]))?(/[smhdwMy])?$",
                default="now/M",
            )
        )
        self.meta.add(
            MetaDataField(
                name="utc",
                kind=MetaData.Type.BOOL,
                description="Time in UTC",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeRunning",
                kind=MetaData.Type.BOOL,
                description="Include running",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="calculatePrediction",
                kind=MetaData.Type.BOOL,
                description="Calculate prediction",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="preference",
                kind=MetaData.Type.UINT,
                description="The request with the highest preference be shown by default",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Administrator notes",
                default='',
            )
        )
        self.baseType = 'ChargeBackRequest'
        self.service_type = self.baseType
        self.allTypes = ['ChargeBackRequest']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

