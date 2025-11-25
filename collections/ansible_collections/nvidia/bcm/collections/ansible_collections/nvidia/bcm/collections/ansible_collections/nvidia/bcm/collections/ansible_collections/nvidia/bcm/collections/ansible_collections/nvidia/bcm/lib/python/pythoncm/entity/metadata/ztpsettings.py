from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ZTPSettings(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ztpScriptTemplate",
                kind=MetaData.Type.STRING,
                description="ZTP script template",
                default="cumulus-ztp.sh",
            )
        )
        self.meta.add(
            MetaDataField(
                name="ztpJsonTemplate",
                kind=MetaData.Type.STRING,
                description="ZTP JSON template for NVOS",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="switchImage",
                kind=MetaData.Type.STRING,
                description="Image loaded via ONIE",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="checkImageOnBoot",
                kind=MetaData.Type.BOOL,
                description="Check image matches on boot, if not clear switch and start from scratch",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="runZtpOnEachBoot",
                kind=MetaData.Type.BOOL,
                description="Run ZTP on each boot",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="watchDisabledZtp",
                kind=MetaData.Type.BOOL,
                description="Watch switch with potential disabled ZTP",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="installLiteDaemon",
                kind=MetaData.Type.BOOL,
                description="Install lite daemon during ZTP",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="authorizedKeyFileRoot",
                kind=MetaData.Type.STRING,
                description="Authorized key file to be copied for root user",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="authorizedKeyFileCumulus",
                kind=MetaData.Type.STRING,
                description="Authorized key file to be copied for cumulus user",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="authorizedKeyFileAdmin",
                kind=MetaData.Type.STRING,
                description="Authorized key file to be copied for admin user",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableAPI",
                kind=MetaData.Type.BOOL,
                description="Enable access to API",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableExternalAccessAPI",
                kind=MetaData.Type.BOOL,
                description="Enable external access to API instead of only localhost",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updateEtcHosts",
                kind=MetaData.Type.BOOL,
                description="Update the /etc/hosts with the BCM master entry",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="firmwares",
                kind=MetaData.Type.STRING,
                description="List of firmwares to check and install",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="preInstallScripts",
                kind=MetaData.Type.STRING,
                description="List of scripts executed at the start of ZTP",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="postInstallScripts",
                kind=MetaData.Type.STRING,
                description="List of scripts executed at the end of ZTP",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ptmTopologyFile",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mergeKeyValueSettingsPartition",
                kind=MetaData.Type.BOOL,
                description="Merge key value settings partition",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="keyValueSettings",
                kind=MetaData.Type.ENTITY,
                description="Key value settings which can be passed to the ZTP script",
                instance='KeyValueSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'ZTPSettings'
        self.service_type = self.baseType
        self.allTypes = ['ZTPSettings']
        self.top_level = False
        self.leaf_entity = True

