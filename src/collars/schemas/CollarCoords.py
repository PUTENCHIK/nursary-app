# from src.collars.schemas.Collar import Collar
from pydantic import BaseModel


class CollarCoords(BaseModel):
    latitude: float
    longitude: float
