from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

load_dotenv()


class AppSettings(BaseSettings):
    # sql table names
    package_table_name: str = 'package'
    types_table_name: str = 'type'
    session_table_name: str = 'session'

    # sql params
    mysql_database: str
    mysql_user: str
    mysql_password: str
    mysql_root_password: str
    mysql_host: str
    mysql_port: int

    # redis params
    redis_host: str
    redis_port: int
    redis_password: str
    redis_base: int

    # app params
    service_host: str
    service_port: int
    secret_key: str
    project_name: str = 'International Delivery'

    class Config:
        env_file = '.env'

    @property
    def mysql_url(self):
        return (f'mysql+asyncmy://{self.mysql_user}:'
                f'{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/'
                f'{self.mysql_database}')

    @property
    def sync_redis_url(self):
        return (f'redis://:{self.redis_password}@{self.redis_host}:'
                f'{self.redis_port}/{self.redis_base}')
