from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class WorkloadPowerProfileSettings(Entity):
    """
    Workload power profile settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disable jobs from changing NVIDIA workload profiles",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="failOnError",
                kind=MetaData.Type.BOOL,
                description="Should prolog and epilog fail when workload power profile change fails",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobKeyword",
                kind=MetaData.Type.STRING,
                description="Keyword used by WLM job to specify the workload profile settings",
                default="wpps",
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobsProfilesDir",
                kind=MetaData.Type.STRING,
                description="Directory where prolog creates job ID directories that include workload power profile subdirectories.",
                default="/var/run/nvidia/workload-power-profiles",
            )
        )
        self.meta.add(
            MetaDataField(
                name="debug",
                kind=MetaData.Type.BOOL,
                description="Enable prolog and epilog debug mode",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="debugLogDir",
                kind=MetaData.Type.STRING,
                description="Debug log directory where prolog and epilog will create log files per job",
                default="/var/spool/cmd/wlm/wpps",
            )
        )
        self.baseType = 'WorkloadPowerProfileSettings'
        self.service_type = self.baseType
        self.allTypes = ['WorkloadPowerProfileSettings']
        self.top_level = False
        self.leaf_entity = True

