import logging

from pydantic_settings import SettingsConfigDict

from .deploy import DeploymentConfig
from .feature import FeatureConfig
from .middleware import MiddlewareConfig
from .packaging import PackagingInfo

logger = logging.getLogger(__name__)


class HiggsConfig(
    PackagingInfo,
    # Deployment configs
    DeploymentConfig,
    # Feature configs
    FeatureConfig,
    # Middleware configs
    MiddlewareConfig,
):
    model_config = SettingsConfigDict(
        # read from dotenv format config file
        env_file=".env",
        env_file_encoding="utf-8",
        # ignore extra attributes
        extra="ignore",
    )
