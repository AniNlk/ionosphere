from fastapi import FastAPI, Depends
from typing import List
from schemas import QueryParabolicNe, ResponseParabolicNe, ResponseChapmanNe, QueryChapmanNe
import numpy as np

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/ne/Parabolic", response_model=List[ResponseParabolicNe])
def parab(
    query: QueryParabolicNe = Depends()
):
    result: List[ResponseParabolicNe] = []
    nm = 1.24 * 10**10 * query.fc_p**2
    hm = query.h0 + query.yb
    h = query.h0
    while h <= hm + query.yb:
        x = h - hm
        ne = nm * (1 - x**2/query.yb**2)
        result.append(ResponseParabolicNe(x=ne, y=h))
        h += 1.0
    return result
@app.get("/ne/Chapman", response_model=List[ResponseChapmanNe])
def chap(
    query: QueryChapmanNe = Depends()
):
    result: List[ResponseChapmanNe] = []
    nm = 1.24 * 10**10 * query.fc_c**2
    h = query.h
    hm = query.hm
    while h <= 4*hm + query.h:
        x = h - hm
        ne = nm * np.exp(1 - x/h - np.exp(-x/h))
        result.append(ResponseChapmanNe(x=ne, y=h))
        h += 1.0
    return result