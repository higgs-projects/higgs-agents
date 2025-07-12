import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# 这是 Alembic 配置（Config）对象，它提供对当前使用的 .ini 配置文件中参数的访问
config = context.config

# 解释 Python 日志配置文件
# 这行代码的作用基本上是设置日志记录器 loggers
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# 在此添加你的模型的 MetaData 对象 以支持 自动生成（autogenerate） 迁移脚本
# User 必须存在，虽然看起来没有使用到，但是这样才会被SQLModel识别到！！！

from configs import higgs_config
from models.base import Base
from models.hero import Hero

def get_metadata():
    return Base.metadata


# env.py 需要的其他配置值可以通过 config 获取, 例如
# my_important_option = config.get_main_option("my_important_option")


def get_url():
    return str(higgs_config.SQLALCHEMY_DATABASE_URI)

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "foreign_key_constraint":
        return False
    else:
        return True

def run_migrations_offline():
    """以离线模式运行迁移。
    在这种情况下，上下文（Context）仅使用数据库 URL 进行配置，而不会创建引擎（Engine），尽管这里也可以使用引擎
    通过跳过引擎的创建，我们甚至不需要数据库驱动（DBAPI）可用
    在此模式下，对 context.execute() 的调用会将指定的 SQL 语句直接输出到迁移脚本中
    """
    url = get_url()
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """以在线模式运行迁移。
    在这种情况下，我们需要创建一个引擎（Engine）并将连接（Connection）与上下文（Context）关联
    """
    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=get_metadata(), 
            process_revision_directives=process_revision_directives,
            include_object=include_object,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
