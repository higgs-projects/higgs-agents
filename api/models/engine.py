from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from configs import higgs_config

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


engine = create_engine(
    url=higgs_config.SQLALCHEMY_DATABASE_URI, 
    echo=higgs_config.SQLALCHEMY_ECHO,
    echo_pool=higgs_config.SQLALCHEMY_ECHO,
    **higgs_config.SQLALCHEMY_ENGINE_OPTIONS,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()