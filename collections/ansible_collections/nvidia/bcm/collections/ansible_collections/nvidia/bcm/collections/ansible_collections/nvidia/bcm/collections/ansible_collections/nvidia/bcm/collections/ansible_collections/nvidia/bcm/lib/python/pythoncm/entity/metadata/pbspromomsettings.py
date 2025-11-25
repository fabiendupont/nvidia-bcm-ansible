from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PbsProMomSettings(Entity):
    """
    PBS pro pbs_mom daemon settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="outputHostname",
                kind=MetaData.Type.STRING,
                description="Host to which all job standard output and standard error are delivered (PBS_OUTPUT_HOST_NAME parameter in pbs.conf)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="leafRouters",
                kind=MetaData.Type.STRING,
                description="Location of endpoint's pbs_comm daemon (PBS_LEAF_ROUTERS parameter in pbs.conf)",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="leafName",
                kind=MetaData.Type.STRING,
                description="Leaf name (PBS_LEAF_NAME parameter in pbs.conf)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="leafManagementFqdn",
                kind=MetaData.Type.BOOL,
                description="Leaf name in pbs.conf is appended with FQDN from management network",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="startMom",
                kind=MetaData.Type.BOOL,
                description="Configure pbs_mom daemon start (PBS_START_MOM parameter in pbs.conf)",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="spool",
                kind=MetaData.Type.STRING,
                description="PBS Pro mom spool directory",
                default='',
            )
        )
        self.baseType = 'PbsProMomSettings'
        self.service_type = self.baseType
        self.allTypes = ['PbsProMomSettings']
        self.top_level = False
        self.leaf_entity = True

