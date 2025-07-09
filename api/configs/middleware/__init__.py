import os
from typing import Any, Literal, Optional
from urllib.parse import parse_qsl, quote_plus

from pydantic import Field, NonNegativeFloat, NonNegativeInt, PositiveFloat, PositiveInt, computed_field
from pydantic_settings import BaseSettings

from .cache.redis_config import RedisConfig
from .storage.aliyun_oss_storage_config import AliyunOSSStorageConfig
from .storage.opendal_storage_config import OpenDALStorageConfig
from .storage.tencent_cos_storage_config import TencentCloudCOSStorageConfig
from .storage.volcengine_tos_storage_config import VolcengineTOSStorageConfig
from .vdb.chroma_config import ChromaConfig
from .vdb.elasticsearch_config import ElasticsearchConfig
from .vdb.milvus_config import MilvusConfig
from .vdb.pgvector_config import PGVectorConfig
from .vdb.pgvectors_config import PGVectoRSConfig
from .vdb.tencent_vector_config import TencentVectorDBConfig
from .vdb.weaviate_config import WeaviateConfig


class StorageConfig(BaseSettings):
    STORAGE_TYPE: Literal[
        "opendal",
        "aliyun-oss",
        "tencent-cos",
        "volcengine-tos",
    ] = Field(
        description="Type of storage to use."
        " Options: 'opendal', 'aliyun-oss',"
        "'tencent-cos', 'volcengine-tos'. Default is 'opendal'.",
        default="opendal",
    )

    STORAGE_LOCAL_PATH: str = Field(
        description="Path for local storage when STORAGE_TYPE is set to 'local'.",
        default="storage",
        deprecated=True,
    )


class VectorStoreConfig(BaseSettings):
    VECTOR_STORE: Optional[str] = Field(
        description="Type of vector store to use for efficient similarity search."
        " Set to None if not using a vector store.",
        default=None,
    )

    VECTOR_STORE_WHITELIST_ENABLE: Optional[bool] = Field(
        description="Enable whitelist for vector store.",
        default=False,
    )


class KeywordStoreConfig(BaseSettings):
    KEYWORD_STORE: str = Field(
        description="Method for keyword extraction and storage."
        " Default is 'jieba', a Chinese text segmentation library.",
        default="jieba",
    )


class DatabaseConfig(BaseSettings):
    DB_HOST: str = Field(
        description="Hostname or IP address of the database server.",
        default="localhost",
    )

    DB_PORT: PositiveInt = Field(
        description="Port number for database connection.",
        default=5432,
    )

    DB_USERNAME: str = Field(
        description="Username for database authentication.",
        default="postgres",
    )

    DB_PASSWORD: str = Field(
        description="Password for database authentication.",
        default="",
    )

    DB_DATABASE: str = Field(
        description="Name of the database to connect to.",
        default="dify",
    )

    DB_CHARSET: str = Field(
        description="Character set for database connection.",
        default="",
    )

    DB_EXTRAS: str = Field(
        description="Additional database connection parameters. Example: 'keepalives_idle=60&keepalives=1'",
        default="",
    )

    SQLALCHEMY_DATABASE_URI_SCHEME: str = Field(
        description="Database URI scheme for SQLAlchemy connection.",
        default="postgresql",
    )

    @computed_field
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        db_extras = (
            f"{self.DB_EXTRAS}&client_encoding={self.DB_CHARSET}" if self.DB_CHARSET else self.DB_EXTRAS
        ).strip("&")
        db_extras = f"?{db_extras}" if db_extras else ""
        return (
            f"{self.SQLALCHEMY_DATABASE_URI_SCHEME}://"
            f"{quote_plus(self.DB_USERNAME)}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
            f"{db_extras}"
        )

    SQLALCHEMY_POOL_SIZE: NonNegativeInt = Field(
        description="Maximum number of database connections in the pool.",
        default=30,
    )

    SQLALCHEMY_MAX_OVERFLOW: NonNegativeInt = Field(
        description="Maximum number of connections that can be created beyond the pool_size.",
        default=10,
    )

    SQLALCHEMY_POOL_RECYCLE: NonNegativeInt = Field(
        description="Number of seconds after which a connection is automatically recycled.",
        default=3600,
    )

    SQLALCHEMY_POOL_PRE_PING: bool = Field(
        description="If True, enables connection pool pre-ping feature to check connections.",
        default=False,
    )

    SQLALCHEMY_ECHO: bool | str = Field(
        description="If True, SQLAlchemy will log all SQL statements.",
        default=False,
    )

    RETRIEVAL_SERVICE_EXECUTORS: NonNegativeInt = Field(
        description="Number of processes for the retrieval service, default to CPU cores.",
        default=os.cpu_count() or 1,
    )

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self) -> dict[str, Any]:
        # Parse DB_EXTRAS for 'options'
        db_extras_dict = dict(parse_qsl(self.DB_EXTRAS))
        options = db_extras_dict.get("options", "")
        # Always include timezone
        timezone_opt = "-c timezone=UTC"
        if options:
            # Merge user options and timezone
            merged_options = f"{options} {timezone_opt}"
        else:
            merged_options = timezone_opt

        connect_args = {"options": merged_options}

        return {
            "pool_size": self.SQLALCHEMY_POOL_SIZE,
            "max_overflow": self.SQLALCHEMY_MAX_OVERFLOW,
            "pool_recycle": self.SQLALCHEMY_POOL_RECYCLE,
            "pool_pre_ping": self.SQLALCHEMY_POOL_PRE_PING,
            "connect_args": connect_args,
        }


class DatasetQueueMonitorConfig(BaseSettings):
    """
    Configuration settings for Dataset Queue Monitor
    """

    QUEUE_MONITOR_THRESHOLD: Optional[NonNegativeInt] = Field(
        description="Threshold for dataset queue monitor",
        default=200,
    )
    QUEUE_MONITOR_ALERT_EMAILS: Optional[str] = Field(
        description="Emails for dataset queue monitor alert, separated by commas",
        default=None,
    )
    QUEUE_MONITOR_INTERVAL: Optional[NonNegativeFloat] = Field(
        description="Interval for dataset queue monitor in minutes",
        default=30,
    )


class MiddlewareConfig(
    # place the configs in alphabet order
    DatabaseConfig,
    KeywordStoreConfig,
    RedisConfig,
    # configs of storage and storage providers
    StorageConfig,
    AliyunOSSStorageConfig,
    OpenDALStorageConfig,
    TencentCloudCOSStorageConfig,
    VolcengineTOSStorageConfig,
    # configs of vdb and vdb providers
    VectorStoreConfig,
    ChromaConfig,
    MilvusConfig,
    PGVectorConfig,
    PGVectoRSConfig,
    TencentVectorDBConfig,
    WeaviateConfig,
    ElasticsearchConfig,
    DatasetQueueMonitorConfig,
):
    pass
