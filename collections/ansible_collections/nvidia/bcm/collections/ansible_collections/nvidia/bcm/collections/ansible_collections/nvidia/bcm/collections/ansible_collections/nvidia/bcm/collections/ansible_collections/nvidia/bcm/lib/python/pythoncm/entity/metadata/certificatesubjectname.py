from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CertificateSubjectName(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="country",
                kind=MetaData.Type.STRING,
                description="Country",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.STRING,
                description="State",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="locality",
                kind=MetaData.Type.STRING,
                description="Locality",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="organization",
                kind=MetaData.Type.STRING,
                description="Organization",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="organizationalUnit",
                kind=MetaData.Type.STRING,
                description="Organizational unit",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="commonName",
                kind=MetaData.Type.STRING,
                description="CommonName",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="profile",
                kind=MetaData.Type.STRING,
                description="Profile",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="syslogin",
                kind=MetaData.Type.STRING,
                description="Syslogin",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="component",
                kind=MetaData.Type.STRING,
                description="Component",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="days",
                kind=MetaData.Type.INT,
                description="Days",
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ca",
                kind=MetaData.Type.BOOL,
                description="CA",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="subjectAlternativeNames",
                kind=MetaData.Type.STRING,
                description="Alternative names",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'CertificateSubjectName'
        self.service_type = self.baseType
        self.allTypes = ['CertificateSubjectName']
        self.top_level = False
        self.leaf_entity = True

