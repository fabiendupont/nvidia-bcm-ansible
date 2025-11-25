from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class WlmCluster(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                regex_check=r"^[^/\s\0]+$",
                required=True,
                diff_type=MetaDataField.Diff.disabled,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="moduleFileTemplate",
                kind=MetaData.Type.STRING,
                description="Template content for system module file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="primaryServer",
                kind=MetaData.Type.RESOLVE,
                description="The WLM primary server (where the active WLM daemon will be running).",
                instance='Node',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="network",
                kind=MetaData.Type.RESOLVE,
                description="Network that will be used to form FQDN node names",
                instance='Network',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="tracingJobs",
                kind=MetaData.Type.STRING,
                description="A list of job ids to trace in CMDaemon",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="enablePreJob",
                kind=MetaData.Type.BOOL,
                description="Enable Cluster Manager powered pre job healthchecking in the workload manager",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enablePostJob",
                kind=MetaData.Type.BOOL,
                description="Enable Cluster Manager powered post job healthchecking in the workload manager",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="accounting",
                kind=MetaData.Type.ENTITY,
                description="Advanced accounting settings",
                instance='WlmAdvancedAccountingSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'WlmCluster'
        self.service_type = self.baseType
        self.allTypes = ['WlmCluster']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

