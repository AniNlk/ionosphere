from pydantic import BaseModel

class QueryParabolicNe(BaseModel):
    h0: float #высота минимума Ne
    yb: float #полуширина слоя
    fc_p: float #максимум электронной концентрации
class QueryChapmanNe(BaseModel):
    fc_c: float
    h: float
    hm: float

class ResponseParabolicNe(BaseModel):
    x: float
    y: float
class ResponseChapmanNe(BaseModel):
    x: float
    y: float