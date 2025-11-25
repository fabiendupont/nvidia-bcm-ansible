from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CertificateRequest(Entity):
    """
    Certificate request
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="CSR",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="session_uuid",
                kind=MetaData.Type.UUID,
                description="Session",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientType",
                kind=MetaData.Type.UINT,
                description="Client type",
                default=0,
            )
        )
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
                description="Common name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="subjectAlternativeNames",
                kind=MetaData.Type.STRING,
                description="Subject alternative names",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowAutosign",
                kind=MetaData.Type.BOOL,
                description="Allow autosign",
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
        self.baseType = 'CertificateRequest'
        self.service_type = self.baseType
        self.allTypes = ['CertificateRequest']
        self.top_level = True
        self.leaf_entity = True
        self.allow_commit = False

