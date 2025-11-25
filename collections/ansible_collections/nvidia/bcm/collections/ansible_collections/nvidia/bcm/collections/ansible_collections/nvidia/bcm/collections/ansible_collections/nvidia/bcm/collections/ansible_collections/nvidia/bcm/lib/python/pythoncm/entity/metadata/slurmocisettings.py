from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SlurmOCISettings(Entity):
    """
    Slurm OCI settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="containerPath",
                kind=MetaData.Type.STRING,
                description="Override path pattern for placement of the generated OCI Container bundle directory.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="createEnvFile",
                kind=MetaData.Type.BOOL,
                description="Create environment file for container.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="runTimeCreate",
                kind=MetaData.Type.STRING,
                description="Pattern for OCI runtime create operation.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="runTimeDelete",
                kind=MetaData.Type.STRING,
                description="Pattern for OCI runtime delete operation.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="runTimeKill",
                kind=MetaData.Type.STRING,
                description="Pattern for OCI runtime kill operation.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="runTimeQuery",
                kind=MetaData.Type.STRING,
                description="Pattern for OCI runtime query operation.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="runTimeRun",
                kind=MetaData.Type.STRING,
                description="Pattern for OCI runtime run operation.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="runTimeStart",
                kind=MetaData.Type.STRING,
                description="Pattern for OCI runtime start operation.",
                default='',
            )
        )
        self.baseType = 'SlurmOCISettings'
        self.service_type = self.baseType
        self.allTypes = ['SlurmOCISettings']
        self.top_level = False
        self.leaf_entity = True

