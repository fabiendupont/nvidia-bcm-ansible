from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SlurmPRSSettings(Entity):
    """
    Slurm PRS settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="certificatePath",
                kind=MetaData.Type.STRING,
                description="Complete path where Slurm can find the certificate it needs to use to contact PRS",
                default="/cm/local/apps/prs/etc/${WLM_NAME}.pem",
            )
        )
        self.meta.add(
            MetaDataField(
                name="privateKeyPath",
                kind=MetaData.Type.STRING,
                description="Complete path where Slurm can find the private key it needs to use to contact PRS",
                default="/cm/local/apps/prs/etc/${WLM_NAME}.key",
            )
        )
        self.baseType = 'SlurmPRSSettings'
        self.service_type = self.baseType
        self.allTypes = ['SlurmPRSSettings']
        self.top_level = False
        self.leaf_entity = True

