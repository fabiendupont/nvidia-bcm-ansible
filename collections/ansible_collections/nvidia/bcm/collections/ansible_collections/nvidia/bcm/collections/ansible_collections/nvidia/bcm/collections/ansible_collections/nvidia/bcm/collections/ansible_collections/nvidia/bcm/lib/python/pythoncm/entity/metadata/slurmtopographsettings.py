from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SlurmTopographSettings(Entity):
    """
    Topograph service integration settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="hostname",
                kind=MetaData.Type.STRING,
                description="Hostname where topograph runs",
                default="localhost",
            )
        )
        self.meta.add(
            MetaDataField(
                name="configPath",
                kind=MetaData.Type.STRING,
                description="Path to topograph configuration file",
                default="/etc/topograph/topograph-config.yaml",
            )
        )
        self.meta.add(
            MetaDataField(
                name="httpParameters",
                kind=MetaData.Type.STRING,
                description="Parameters string that is passed to the service HTTP API",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="passCloudCredentials",
                kind=MetaData.Type.BOOL,
                description="Specifies whether the CSP credentials will be passed to the topology generator",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fetchTimeout",
                kind=MetaData.Type.UINT,
                description="Topograph API timeout",
                default=20,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fetchAttempts",
                kind=MetaData.Type.UINT,
                description="Number of attempts to get topology from topograph",
                default=12,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fetchWaitTime",
                kind=MetaData.Type.UINT,
                description="Wait time in seconds between fetching attempts",
                default=15,
            )
        )
        self.baseType = 'SlurmTopographSettings'
        self.service_type = self.baseType
        self.allTypes = ['SlurmTopographSettings']
        self.top_level = False
        self.leaf_entity = True

