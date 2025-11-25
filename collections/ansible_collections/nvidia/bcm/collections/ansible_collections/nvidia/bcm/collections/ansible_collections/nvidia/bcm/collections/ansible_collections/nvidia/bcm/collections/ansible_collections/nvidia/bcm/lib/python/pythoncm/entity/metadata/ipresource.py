from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.basicresource import BasicResource


class IPResource(BasicResource):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ip",
                kind=MetaData.Type.STRING,
                description="IP",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="networkDeviceName",
                kind=MetaData.Type.STRING,
                description="The network device name to start this IP on. Leave blank to automatically determine based on IP.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="alias",
                kind=MetaData.Type.STRING,
                description="The network device name alias",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.UINT,
                description="Timeout",
                default=5,
            )
        )
        self.baseType = 'BasicResource'
        self.childType = 'IPResource'
        self.service_type = self.baseType
        self.allTypes = ['IPResource', 'BasicResource']
        self.top_level = False
        self.leaf_entity = True

