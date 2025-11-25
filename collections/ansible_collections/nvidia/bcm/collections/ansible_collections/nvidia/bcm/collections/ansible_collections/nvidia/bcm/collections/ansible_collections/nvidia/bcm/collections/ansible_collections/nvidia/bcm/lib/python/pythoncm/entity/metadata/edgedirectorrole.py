from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.directorrole import DirectorRole


class EdgeDirectorRole(DirectorRole):
    """
    Edge director role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nodePowerOperations",
                kind=MetaData.Type.BOOL,
                description="Execute all power operations of nodes in the edge site on the director",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="directorPowerOperations",
                kind=MetaData.Type.BOOL,
                description="Execute all power operation of the director on the director, note that this means it cannot be powered on",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeSelectionBootRole",
                kind=MetaData.Type.BOOL,
                description="Use the edge site as a node selection mechanism for the boot role",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeSelectionDnsRole",
                kind=MetaData.Type.BOOL,
                description="Use the edge site as a node selection mechanism for the DNS role",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeSelectionProvisioningRole",
                kind=MetaData.Type.BOOL,
                description="Use the edge site as a node selection mechanism for the provisioning role",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="addNamedService",
                kind=MetaData.Type.BOOL,
                description="Add named service to the node",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="addSlapdService",
                kind=MetaData.Type.BOOL,
                description="Add slapd service to the node",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="addNtpdService",
                kind=MetaData.Type.BOOL,
                description="Add ntpd service to the node",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="openTCPPortsOnHeadNode",
                kind=MetaData.Type.INT,
                description="The list of TCP ports that will be opened in shorewall on the head node",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="openUDPPortsOnHeadNode",
                kind=MetaData.Type.INT,
                description="The list of UDP ports that will be opened in shorewall on the head node",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="externallyVisibleIp",
                kind=MetaData.Type.STRING,
                description="IP that will be seen by other nodes when the director connects",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="externallyVisibleHeadNodeIp",
                kind=MetaData.Type.STRING,
                description="Head node IP that will be use by this director",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="syncCmShared",
                kind=MetaData.Type.BOOL,
                description="Sync /cm/shared if required",
                default=True,
            )
        )
        self.baseType = 'Role'
        self.childType = 'EdgeDirectorRole'
        self.service_type = self.baseType
        self.allTypes = ['EdgeDirectorRole', 'DirectorRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

