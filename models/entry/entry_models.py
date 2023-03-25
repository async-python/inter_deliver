from uuid import UUID

from pydantic import Field

from models.base_model import OrjsonBase


class PackageEntry(OrjsonBase):
    name: str
    weight: float = Field(gt=0)
    type_id: int
    usd_price: float = Field(gt=0)


class PackageDb(PackageEntry):
    session_id: UUID
