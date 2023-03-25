from typing import Optional, Union

from models.base_model import OrjsonBase


class TypesOut(OrjsonBase):
    id: int
    name: str


class PackageIdOut(OrjsonBase):
    id: int


class PackageDetailShortOut(OrjsonBase):
    """Данные включают: название, вес, тип посылки,
    ее стоимость, стоимость доставки."""
    name: str
    weight: float
    type: int
    delivery_cost: Union[str, float]


class PackageDetailFullOut(OrjsonBase):
    """Получить список своих посылок со всеми полями, включая имя типа посылки
    и стоимость доставки (если она уже рассчитана)."""
    name: str
    weight: float
    type_name: str
    usd_price: float
    delivery_cost: Optional[float]
