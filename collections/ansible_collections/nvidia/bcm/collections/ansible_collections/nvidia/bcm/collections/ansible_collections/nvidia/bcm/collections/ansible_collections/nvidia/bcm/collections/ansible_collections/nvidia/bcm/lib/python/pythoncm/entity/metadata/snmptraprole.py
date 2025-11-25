from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class SnmpTrapRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="event",
                kind=MetaData.Type.BOOL,
                description="Enable events",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mail",
                kind=MetaData.Type.BOOL,
                description="Enable mail",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="recipients",
                kind=MetaData.Type.STRING,
                description="Recipients",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="allAdministrators",
                kind=MetaData.Type.BOOL,
                description="Also send e-mail to all administrators as defined in partition",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="access",
                kind=MetaData.Type.STRING,
                description="Access string",
                default="public",
            )
        )
        self.meta.add(
            MetaDataField(
                name="server",
                kind=MetaData.Type.STRING,
                description="The SNMP server",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sender",
                kind=MetaData.Type.STRING,
                description="The sender of the e-mail",
                function_check=MetaData.check_isEmail,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="arguments",
                kind=MetaData.Type.STRING,
                description="Additional script arguments",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="alternativeScript",
                kind=MetaData.Type.STRING,
                description="Alternative script",
                default='',
            )
        )
        self.baseType = 'Role'
        self.childType = 'SnmpTrapRole'
        self.service_type = self.baseType
        self.allTypes = ['SnmpTrapRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

