from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class RemoteSetupExecution(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="id",
                kind=MetaData.Type.INT,
                description="A unique identified of the remote cm-*-setup execution.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="inputConfig",
                kind=MetaData.Type.STRING,
                description="cm-*-setup yaml input configuration file (used with '-c' flag).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="exitCode",
                kind=MetaData.Type.INT,
                description="The return exit code from cm-setup (once the execution has been completed.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="signal",
                kind=MetaData.Type.INT,
                description="Number identifying the signal which interrupted the execution.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="datacout",
                kind=MetaData.Type.STRING,
                description="Data which was emitted on stdout from cm-*-setup.",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'RemoteSetupExecution'
        self.service_type = self.baseType
        self.allTypes = ['RemoteSetupExecution']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

