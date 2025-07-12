from sqlmodel import MetaData, Session, create_engine

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


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()