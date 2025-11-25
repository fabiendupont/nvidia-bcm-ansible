from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class User(Entity):
    """
    User
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="User login (e.g. donald)",
                regex_check=r"^[a-zA-Z_]([.a-zA-Z0-9_-]{0,31}|[.a-zA-Z0-9_-]{0,30}\$)$",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ID",
                kind=MetaData.Type.STRING,
                description="User ID number",
                regex_check=r"^(|\d+)$",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="commonName",
                kind=MetaData.Type.STRING,
                description="Full name (e.g. Donald Duck)",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="surname",
                kind=MetaData.Type.STRING,
                description="Surname (e.g. Duck)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="groupID",
                kind=MetaData.Type.STRING,
                description="Base group of this user",
                regex_check=r"^(|\d+)$",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="loginShell",
                kind=MetaData.Type.STRING,
                description="Login shell",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="homeDirectory",
                kind=MetaData.Type.STRING,
                description="Home directory",
                regex_check=r"^(|/.*)$",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="password",
                kind=MetaData.Type.STRING,
                description="Password",
                diff_type=MetaDataField.Diff.crypt_hash,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="homeDirOperation",
                kind=MetaData.Type.BOOL,
                description="Set to false to not create or move home directory",
                diff_type=MetaDataField.Diff.none,
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="shadowMin",
                kind=MetaData.Type.UINT,
                description="Minimum number of days required between password changes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="shadowMax",
                kind=MetaData.Type.UINT,
                description="Maximum number of days for which the user password remains valid.",
                default=999999,
            )
        )
        self.meta.add(
            MetaDataField(
                name="shadowWarning",
                kind=MetaData.Type.UINT,
                description="Number of days of advance warning given to the user before the user password expires",
                default=7,
            )
        )
        self.meta.add(
            MetaDataField(
                name="shadowInactive",
                kind=MetaData.Type.UINT,
                description="Number of days of inactivity allowed for the user",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="shadowLastChange",
                kind=MetaData.Type.UINT,
                description="Number of days between January 1, 1970 and the day when the user password was last changed",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="shadowExpire",
                kind=MetaData.Type.UINT,
                description="Date on which the user login will be disabled",
                default=24837,
            )
        )
        self.meta.add(
            MetaDataField(
                name="email",
                kind=MetaData.Type.STRING,
                description="Email",
                function_check=MetaData.check_isEmail,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="profile",
                kind=MetaData.Type.STRING,
                description="Profile for Authorization",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="certSerialNumber",
                kind=MetaData.Type.INT,
                description="Serial number of the certificate assigned to user",
                readonly=True,
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="projectManager",
                kind=MetaData.Type.ENTITY,
                description="Project manager",
                instance='ProjectManager',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Administrator notes",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="homePage",
                kind=MetaData.Type.STRING,
                description="Home page",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="information",
                kind=MetaData.Type.STRING,
                description="Information added by CMDaemon",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="writeSshProxyConfig",
                kind=MetaData.Type.BOOL,
                description="Write ssh proxy config",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="createSshKey",
                kind=MetaData.Type.BOOL,
                description="Create ssh key for added users",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disablePasswordSsh",
                kind=MetaData.Type.BOOL,
                description="Disable password ssh",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="authorizedSshKeys",
                kind=MetaData.Type.STRING,
                description="Authorized ssh keys",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowGPUWorkloadPowerProfiles",
                kind=MetaData.Type.BOOL,
                description="Allow changing GPU workload power profiles from jobs",
                default=False,
            )
        )
        self.baseType = 'User'
        self.service_type = self.baseType
        self.allTypes = ['User']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

