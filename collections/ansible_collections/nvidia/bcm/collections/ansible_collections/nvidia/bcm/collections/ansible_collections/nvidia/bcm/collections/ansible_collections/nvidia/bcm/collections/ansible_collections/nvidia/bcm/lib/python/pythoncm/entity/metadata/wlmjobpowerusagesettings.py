from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class WlmJobPowerUsageSettings(Entity):
    """
    Workload management job power usage settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disable power usage calculation",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobAge",
                kind=MetaData.Type.UINT,
                description="Job complation age before power is calculated",
                default=300,
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.UINT,
                description="Plot timeout",
                default=30,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodePowerMetrics",
                kind=MetaData.Type.RESOLVE,
                description="Preference of metrics to use for calculating the power usage for the entire node",
                instance='MonitoringMeasurableMetric',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpuPowerMetrics",
                kind=MetaData.Type.RESOLVE,
                description="Preference of metrics to use for calculating the GPU power usage",
                instance='MonitoringMeasurableMetric',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpuPowerMetrics",
                kind=MetaData.Type.RESOLVE,
                description="Preference of metrics to use for calculating the CPU power usage",
                instance='MonitoringMeasurableMetric',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerUnderAllocationMetrics",
                kind=MetaData.Type.RESOLVE,
                description="All metrics that indicate if a device was allocated insufficient power",
                instance='MonitoringMeasurableMetric',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'WlmJobPowerUsageSettings'
        self.service_type = self.baseType
        self.allTypes = ['WlmJobPowerUsageSettings']
        self.top_level = False
        self.leaf_entity = True

