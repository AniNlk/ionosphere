"""
Солнечный терминатор

старт: 31.07.2024
место: Иркутский радар НР, ИСЗФ СО РАН, Иркутск
"""

import uvicorn
from datetime import datetime

from fastapi import FastAPI, Depends
from shemas import ResponseCoord, QueryDateTime, Coordinate
from typing import List
from skyfield.api import load, wgs84

import numpy as np

from skyfield_sun_2 import run_terminator
import matplotlib.pyplot as plt


app = FastAPI(docs_url='/docs')


# def sun_shine(data):
#     """
#
#     :param data: дата в формате
#     :return:
#     """
#     return


@app.get("/get_coordinates", response_model=ResponseCoord)
def get_coordinates(
        query: QueryDateTime=Depends()):

    """
    Получение координат солнечного терминатора

    :param query: дата и время
    :return: координаты в формате широта-долгота
    """

    # result: ResponseCoord = ResponseCoord()

    dt_str = f"{query.data} {query.time}"
    formatted_datetime = datetime.strptime(dt_str, "%Y-%m-%d %H-%M-%S")

    day = query.data
    time = query.time

    ts = load.timescale()
    # t = Time(formatted_datetime)

    # переход к времени для skyfield
    year, month, day = map(int, day.split('-'))
    hour, minute, second = map(int, time.split('-'))

    t1 = ts.utc(year, month, day, hour, minute)

    # положение солнца
    sun_position = []  # извлекаем из файла

    our_terminator = run_terminator(t1)
    print(our_terminator)

    terminator_coordinates = our_terminator['terminator']
    sun_position = [our_terminator['sun']]
    print(sun_position)
    # print(run_terminator(t1))

    terminator_coordinates2 = np.array(terminator_coordinates)
    # Используем scatter для построения графика с точками
    plt.scatter(terminator_coordinates2[:, 0], terminator_coordinates2[:, 1], color='green', s=20,
                label='граница тени')  # s - размер точек
    plt.title("Солнечный терминатор")
    # plt.xlim(-180, 180)
    # plt.ylim(-90, 90)
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.grid()
    plt.legend()  # Добавляем легенду, если это необходимо
    plt.show()
    sun_position_itog = [Coordinate(latitude=lat, longitude=lon) for lon, lat in sun_position]
    terminator_coordinates_itog = [Coordinate(latitude=lat, longitude=lon) for lon, lat in terminator_coordinates]

    return ResponseCoord(sun_position=sun_position_itog, terminator_coordinates=terminator_coordinates_itog)

    # for i in terminator_coordinates:
    #     result.append(ResponseCoord(latitude=i[1], longitude=i[0]))
    # return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

