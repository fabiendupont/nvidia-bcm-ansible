from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Certificate(Entity):
    """
    Certificate
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="PEM",
                kind=MetaData.Type.STRING,
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="revoked",
                kind=MetaData.Type.BOOL,
                description="Certifcate has been revoked and can not be used",
                readonly=True,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="serialNumber",
                kind=MetaData.Type.INT,
                description="Serial number",
                readonly=True,
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="remaining",
                kind=MetaData.Type.INT,
                description="Remaining time until certifcate expires",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Date when certificate is valid",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="expireTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Date when certificate expires",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="CA",
                kind=MetaData.Type.BOOL,
                description="A CA certifcate can be used sign other certifcates",
                readonly=True,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hasEdgeSecret",
                kind=MetaData.Type.BOOL,
                description="Has an edge secret",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="profile",
                kind=MetaData.Type.STRING,
                description="Profile",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sysLogin",
                kind=MetaData.Type.STRING,
                description="System log in ",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="component",
                kind=MetaData.Type.STRING,
                description="Component",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="subjectName",
                kind=MetaData.Type.STRING,
                description="Subject",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="issuerName",
                kind=MetaData.Type.STRING,
                description="Issuer",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="subjectAlternativeNames",
                kind=MetaData.Type.STRING,
                description="Alternative names",
                readonly=True,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="country",
                kind=MetaData.Type.STRING,
                description="Country",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.STRING,
                description="State",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="locality",
                kind=MetaData.Type.STRING,
                description="Locality",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="organization",
                kind=MetaData.Type.STRING,
                description="Organization",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="organizationalUnit",
                kind=MetaData.Type.STRING,
                description="Organizational unit",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="commonName",
                kind=MetaData.Type.STRING,
                description="Name",
                readonly=True,
                default='',
            )
        )
        self.baseType = 'Certificate'
        self.service_type = self.baseType
        self.allTypes = ['Certificate']
        self.top_level = True
        self.leaf_entity = True
        self.allow_commit = False

