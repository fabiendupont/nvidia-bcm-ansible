from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CertificateInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="certificate",
                kind=MetaData.Type.ENTITY,
                description="Certificate",
                instance='Certificate',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="private_key",
                kind=MetaData.Type.STRING,
                description="Optional private key field.",
                readonly=True,
                default='',
            )
        )
        self.baseType = 'CertificateInfo'
        self.service_type = self.baseType
        self.allTypes = ['CertificateInfo']
        self.top_level = False
        self.leaf_entity = True

