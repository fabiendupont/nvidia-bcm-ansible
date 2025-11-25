from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class EC2VPC(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="User-defined name of the VPC",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="vpcID",
                kind=MetaData.Type.STRING,
                description="AWS VPC identifier",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultImageId",
                kind=MetaData.Type.STRING,
                description="ID of the default AMI to start instances with ('latest' means using the latest AMI)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mainRouteTable",
                kind=MetaData.Type.STRING,
                description="Main route table AWS ID",
                readonly=True,
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="publicACL",
                kind=MetaData.Type.STRING,
                description="Public Network ACL ID of the public subnet (cloud director)",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="privateACL",
                kind=MetaData.Type.STRING,
                description="Private Network ACL ID of the private subnet (cloud node)",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultACL",
                kind=MetaData.Type.STRING,
                description="Default network access controll list ID",
                readonly=True,
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="internetGatewayID",
                kind=MetaData.Type.STRING,
                description="The AWS ID of the internet gateway assigned to this VPC",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="region",
                kind=MetaData.Type.RESOLVE,
                description="AWS region of the VPC",
                instance='EC2Region',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="subnets",
                kind=MetaData.Type.RESOLVE,
                description="Subnets (networks) associated with the VPC",
                clone=False,
                instance='Network',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="baseAddress",
                kind=MetaData.Type.STRING,
                description="Base IP address of the VPC",
                function_check=MetaData.check_isIP,
                default="10.0.0.0",
            )
        )
        self.meta.add(
            MetaDataField(
                name="netmaskBits",
                kind=MetaData.Type.INT,
                description="Number of netmask bits",
                default=16,
            )
        )
        self.meta.add(
            MetaDataField(
                name="securityGroupNode",
                kind=MetaData.Type.STRING,
                description="Security group ID of the cloud nodes",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="securityGroupDirector",
                kind=MetaData.Type.STRING,
                description="Security group ID of the cloud director",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="routeTableIdPublic",
                kind=MetaData.Type.STRING,
                description="Routing table ID for the public subnet",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="routeTableIdPrivate",
                kind=MetaData.Type.STRING,
                description="Routing table ID for private subnets",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="setDirectorAsDefaultGateway",
                kind=MetaData.Type.BOOL,
                description="If specified, a default route via the director will be created in the private subnet. This is not necessary if the private subnet was already configured and the nodes have access to the head node (e.g Direct Connect)",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="useInternalIPForDirectorIP",
                kind=MetaData.Type.BOOL,
                description="If specified, CMDaemon will use cloud director's internal IP, instead of a public/external IP. Useful when you have existing IP connectivity to your VPC.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enforceDirectorIP",
                kind=MetaData.Type.STRING,
                description="If specified, CMDaemon will assume this is the cloud director's IP address.",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.baseType = 'EC2VPC'
        self.service_type = self.baseType
        self.allTypes = ['EC2VPC']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

