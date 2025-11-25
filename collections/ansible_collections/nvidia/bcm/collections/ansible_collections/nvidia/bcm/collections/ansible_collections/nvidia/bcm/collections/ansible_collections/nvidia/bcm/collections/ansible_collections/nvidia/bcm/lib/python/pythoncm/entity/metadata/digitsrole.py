from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class DIGITSRole(Role):
    """
    DIGITS service
    """
    class LogLevel(Enum):
        DEBUG = auto()
        INFO = auto()
        WARNING = auto()
        ERROR = auto()
        CRITICAL = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.STRING,
                description="DIGITS version",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                description="DIGITS port",
                default=5000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobsDir",
                kind=MetaData.Type.STRING,
                description="Location where job files are stored. Defined in DIGITS_JOBS_DIR",
                default="$DIGITS_ROOT/digits/jobs",
            )
        )
        self.meta.add(
            MetaDataField(
                name="logfileFilename",
                kind=MetaData.Type.STRING,
                description="File for saving log messages. Defined in DIGITS_LOGFILE_FILENAME",
                default="$DIGITS_ROOT/digits/digits.log",
            )
        )
        self.meta.add(
            MetaDataField(
                name="logfileLevel",
                kind=MetaData.Type.ENUM,
                description="Minimum log message level to be saved (DEBUG/INFO/WARNING/ERROR/CRITICAL). Defined in DIGITS_LOGFILE_LEVEL",
                options=[
                    self.LogLevel.DEBUG,
                    self.LogLevel.INFO,
                    self.LogLevel.WARNING,
                    self.LogLevel.ERROR,
                    self.LogLevel.CRITICAL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.LogLevel,
                default=self.LogLevel.INFO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="serverName",
                kind=MetaData.Type.STRING,
                description="The name of the server (accessible in the UI under 'Info'). Default is the system hostname. Defined in DIGITS_SERVER_NAME",
                default="$hostname",
            )
        )
        self.meta.add(
            MetaDataField(
                name="modelStoreUrl",
                kind=MetaData.Type.STRING,
                description="A list of URL's, separated by comma. Default is the official NVIDIA store. Defined in DIGITS_MODEL_STORE_URL",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="urlPrefix",
                kind=MetaData.Type.STRING,
                description="A path to prepend before every URL. Sets the home-page to be at 'http://localhost/custom-prefix' instead of 'http://localhost/'. Defined in DIGITS_URL_PREFIX",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="caffeRoot",
                kind=MetaData.Type.STRING,
                description="Path to your local Caffe build. Should contain build/tools/caffe and python/caffe/. Defined in CAFFE_ROOT",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="torchRoot",
                kind=MetaData.Type.STRING,
                description="Path to your local Torch build. Should contain install/bin/th. Defined in TORCH_ROOT",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="tensorflowRoot",
                kind=MetaData.Type.STRING,
                description="Path to your local TensorFlow build. Defined in TENSORFLOW_ROOT",
                default="",
            )
        )
        self.baseType = 'Role'
        self.childType = 'DIGITSRole'
        self.service_type = self.baseType
        self.allTypes = ['DIGITSRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

