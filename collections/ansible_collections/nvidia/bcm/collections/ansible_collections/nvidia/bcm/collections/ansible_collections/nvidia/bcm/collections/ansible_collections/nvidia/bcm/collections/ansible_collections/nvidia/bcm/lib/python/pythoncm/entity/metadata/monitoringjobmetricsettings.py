from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringJobMetricSettings(Entity):
    class SamplingType(Enum):
        BRIGHT = auto()
        PROMETHEUS = auto()
        BOTH = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="excludeDevices",
                kind=MetaData.Type.STRING,
                description="Exclude block devices from metric collection (by default all the devices are sampled)",
                vector=True,
                default=["loop","sr"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeDevices",
                kind=MetaData.Type.STRING,
                description="Only these devices will be sampled if the set is not empty",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableAdvancedMetrics",
                kind=MetaData.Type.BOOL,
                description="Sample advanced metrics as well as basic metrics",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mapJobsToGpus",
                kind=MetaData.Type.BOOL,
                description="Associate job with GPUs where the job processes run when possible",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeMetrics",
                kind=MetaData.Type.STRING,
                description="Exclude metrics by name from collection",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeMetrics",
                kind=MetaData.Type.STRING,
                description="Only these metrics will be samples if the set is not empty",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeScripts",
                kind=MetaData.Type.STRING,
                description="Exclude extra scripts from being executed",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeScripts",
                kind=MetaData.Type.STRING,
                description="Only these scripts will be samples if the set is not empty",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="cgroupBaseDirectory",
                kind=MetaData.Type.STRING,
                description="CGroup base directory",
                default="/sys/fs/cgroup",
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraScriptsDirectory",
                kind=MetaData.Type.STRING,
                description="Extra scripts directory",
                default="/cm/local/apps/cmd/scripts/metrics/jobs",
            )
        )
        self.meta.add(
            MetaDataField(
                name="keepAliveSleep",
                kind=MetaData.Type.FLOAT,
                description="Time the cgroup keepalive process sleeps",
                default=3600 * 24 * 56,
            )
        )
        self.meta.add(
            MetaDataField(
                name="samplingType",
                kind=MetaData.Type.ENUM,
                description="Type of metrics sampling",
                options=[
                    self.SamplingType.BRIGHT,
                    self.SamplingType.PROMETHEUS,
                    self.SamplingType.BOTH,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.SamplingType,
                default=self.SamplingType.BOTH,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pickupInterval",
                kind=MetaData.Type.FLOAT,
                description="High initial pickup interval",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pickupTimes",
                kind=MetaData.Type.UINT,
                description="Number of times to apply the high initial pickup interval",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pickupPriority",
                kind=MetaData.Type.UINT,
                description="Priority of the pickup interval change",
                default=50,
            )
        )
        self.baseType = 'MonitoringJobMetricSettings'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringJobMetricSettings']
        self.top_level = False
        self.leaf_entity = True

