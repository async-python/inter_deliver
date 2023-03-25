from uuid import uuid4

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        func)
from sqlalchemy.orm import declarative_base, relationship

from core.config import AppSettings
from utils.mysql_uuid import BinaryUUID

settings = AppSettings()

Base = declarative_base()


class SqlBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PackageSql(SqlBase):
    __tablename__ = settings.package_table_name

    name = Column(String(length=100), nullable=False)
    weight = Column(Float, nullable=False)
    type_id = Column(Integer, ForeignKey(f'{settings.types_table_name}.id'))
    usd_price = Column(Float, nullable=False)
    cost = Column(Float, nullable=True)
    session_id = Column(
        BinaryUUID,
        ForeignKey(f'{settings.session_table_name}.id', ondelete='CASCADE'))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(),
        server_onupdate=func.now())

    session = relationship('SessionSql', back_populates='packages')
    type = relationship('TypeSql', back_populates='packages')


class TypeSql(SqlBase):
    __tablename__ = settings.types_table_name

    name = Column(String(length=100), nullable=False, unique=True)
    packages = relationship('PackageSql', back_populates='type')


class SessionSql(SqlBase):
    __tablename__ = settings.session_table_name

    id = Column(BinaryUUID, primary_key=True, nullable=False,
                unique=True, default=uuid4)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    packages = relationship('PackageSql', back_populates='session')
