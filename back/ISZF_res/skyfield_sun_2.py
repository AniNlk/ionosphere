from skyfield.api import load, wgs84
import numpy as np
from skyfield.positionlib import Geocentric


def cross_product_matrix(a):
    """ computes the cross product matrix

    see https://en.wikipedia.org/wiki/Cross_product#Conversion_to_matrix_multiplication
    code from https://stackoverflow.com/questions/66707295/numpy-cross-product-matrix-function
    """
    return np.cross(a, np.identity(3) * -1)


def rotation_matrix_around_axis(axis_vector, rotation_degrees):
    """ creates a rotation matrix that rotates around a given axis

    see https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
    """
    rotation_radians = rotation_degrees / 180 * np.pi
    return (
        np.cos(rotation_radians) * np.identity(3)
        + np.sin(rotation_radians) * cross_product_matrix(axis_vector)
        + (1 - np.cos(rotation_radians)) * np.outer(axis_vector, axis_vector)
        )


def run_terminator(t):
    eph = load('de421.bsp')
    earth = eph['earth']  # vector from solar system barycenter to geocenter
    sun = eph['sun']  # vector from solar system barycenter to sun
    geocentric_sun = sun - earth  # vector from geocenter to sun

    ts = load.timescale()
    # t = ts.utc(2021, 12, 22, 12, 0)

    sun_subpoint = wgs84.subpoint(geocentric_sun.at(t))  # subpoint method requires a geocentric position

    print('subpoint latitude: ', sun_subpoint.latitude.degrees)
    print('subpoint longitude: ', sun_subpoint.longitude.degrees)

    terminator_angle_from_sun = 90.833 # 90 degrees + sun's semidiameter + refraction at horizon

    sun_vec = geocentric_sun.at(t).position.au # numpy array of sun's position vector
    normal_vec = np.cross(sun_vec, np.array([1,0,0]))# vector normal to sun position and x-axis
    first_terminator_vec = rotation_matrix_around_axis(normal_vec, terminator_angle_from_sun) @ sun_vec # arbitrary first position on terminator

    terminator_latitudes = []
    terminator_longitudes = []

    num_points_on_terminator = 100
    for angle in np.linspace(0, 360, num_points_on_terminator):
        terminator_vector = rotation_matrix_around_axis(sun_vec, angle) @ first_terminator_vec
        terminator_position = Geocentric(terminator_vector, t=t)
        geographic_position = wgs84.subpoint(terminator_position)
        terminator_latitudes.append(geographic_position.latitude.degrees)
        terminator_longitudes.append(geographic_position.longitude.degrees)

    terminator_latitudes = np.array(terminator_latitudes)
    terminator_longitudes = np.array(terminator_longitudes)

    terminator_coordinates = []
    for i in range(len(terminator_latitudes)):
        terminator_coordinates += [[terminator_longitudes[i], terminator_latitudes[i]]]

    result = {'terminator': terminator_coordinates, 'sun': [sun_subpoint.longitude.degrees, sun_subpoint.latitude.degrees]}

    print(result)
    return result


day = '2022-06-22'
time = '12-00-00'
# dt_str = f"{day} {time}"
#
# formatted_datetime = datetime.strptime(dt_str, "%Y-%m-%d %H-%M-%S")
ts = load.timescale()
# t = Time(formatted_datetime)

# переход к времени для skyfield
year, month, day = map(int, day.split('-'))
hour, minute, second = map(int, time.split('-'))

t1 = ts.utc(year, month, day, hour, minute)

print(t1)
# print(t)
# terminator_coordinates = run_terminator(t1)
#
# terminator_coordinates2 = np.array(terminator_coordinates)
# # Используем scatter для построения графика с точками
# plt.scatter(terminator_coordinates2[:, 0], terminator_coordinates2[:, 1], color='green', s=20, label='граница тени')  # s - размер точек
# plt.title("Солнечный терминатор")
# # plt.xlim(-180, 180)
# # plt.ylim(-90, 90)
# plt.xlabel("latitude")
# plt.ylabel("lon")
# plt.grid()
# plt.legend()  # Добавляем легенду, если это необходимо
# plt.show()

# fig, ax = plt.subplots()
# ax.scatter(terminator_coordinates[0], terminator_coordinates[1])
# # ax.scatter(sun_subpoint.longitude.degrees, sun_subpoint.latitude.degrees)
# ax.grid(True)
# plt.show()
