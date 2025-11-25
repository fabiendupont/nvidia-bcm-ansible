from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiJob(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_wlm_cluster_uuid",
                kind=MetaData.Type.UUID,
                description="WlmCluster",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_jobqueue_uuid",
                kind=MetaData.Type.UUID,
                description="Queue",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobID",
                kind=MetaData.Type.STRING,
                description="Job ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="user",
                kind=MetaData.Type.STRING,
                description="User",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="runtime",
                kind=MetaData.Type.UINT,
                description="Runtime",
                default=0,
            )
        )
        self.baseType = 'GuiJob'
        self.service_type = self.baseType
        self.allTypes = ['GuiJob']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

