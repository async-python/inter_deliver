from abc import ABC
from uuid import UUID

from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.types import TypeDecorator


class BinaryUUID(TypeDecorator, ABC):

    impl = BINARY(16)

    def process_bind_param(self, value, dialect):
        try:
            return value.bytes
        except AttributeError:
            try:
                return UUID(value).bytes
            except TypeError:
                return value

    def process_result_value(self, value, dialect):
        return UUID(bytes=value)
