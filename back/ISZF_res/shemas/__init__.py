from pydantic import BaseModel
from typing import List


class QueryDateTime(BaseModel):
    """
    Входные параметры дата и время
    """
    data: str = '2024-07-31'
    time: str = '00-00-00'


class Coordinate(BaseModel):
    """
    Выходной параметр широта-долгота для одной точки
    """
    latitude: float
    longitude: float


class ResponseCoord(BaseModel):
    """
    Выходной параметр

    sun_position - положение Солнца
    terminator_coordinates - координаты солнечного терминатора
    """
    sun_position: List[Coordinate]
    terminator_coordinates: List[Coordinate]
    # coordinates: list = []
