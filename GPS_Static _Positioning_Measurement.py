import math
from typing import List
import numpy as np
def dms_to_rad(dms:List[str]):
    degree, minute, second = dms
    degree = float(degree)
    minute = float(minute) / 60
    second = float(second) / 3600
    total_degree = degree + minute + second
    radian = math.radians(total_degree)
    return radian


def CoordinateTransformation(benchmark, testpoint):
    # benchmark: [['degree', 'min', 'second'], ['degree', 'min', 'second']]
    # testpoint: [['degree', 'min', 'second'], ['degree', 'min', 'second']]
    # return: distance
    a = 6378135
    b = 6356750.5
    e = math.sqrt(1 - (b/a)**2)
    
    benchmark_lon_rad, benchmark_lat_rad = dms_to_rad(benchmark[0]), dms_to_rad(benchmark[1])
    print('benchmark longitude radian:', benchmark_lon_rad, '\t', 'benchmark latitude radian:', benchmark_lat_rad)
    testpoint_lon_rad, testpoint_lat_rad = dms_to_rad(testpoint[0]), dms_to_rad(testpoint[1])
    print('testpoint longitude radian:', testpoint_lon_rad, '\t', 'testpoint latitude radian:', testpoint_lat_rad)

    Kx = a * math.cos(benchmark_lat_rad) / (math.sqrt(1 - e**2 * math.sin(benchmark_lat_rad)**2))
    Ky = a * (1 - e**2) / (1 - e**2 * math.sin(benchmark_lat_rad)**2)**(3/2)

    detx = Kx * (testpoint_lon_rad - benchmark_lon_rad)
    dety = Ky * (testpoint_lat_rad - benchmark_lat_rad)

    distance = math.sqrt(detx**2 + dety**2)
    print('detx:', detx, '\t', 'dety:', dety, '\t', 'distance:', distance)
    return distance

def calculate_mean_std(distances):
    mean = np.mean(distances)
    std = np.std(distances)
    print('mean:', mean, 'std:', std)
    return mean, std

def cal_error(mean: float, std: float):
    RMS = mean + std
    SD = mean + 2 * std
    CEP = mean + 0.68 * std
    return round(RMS, 3), round(SD, 3), round(CEP, 3)
if __name__ == '__main__':
    # input('Please input the benchmark point: ')
    benchmark = []
    benchmark.append(input('Please input the benchmark point longitude: ').split())
    benchmark.append(input('Please input the benchmark point latitude: ').split())
    distances = []
    while True:
        print('if you want to end this program, please input "yes", otherwise, please input the test point')
        if input() == 'yes':
            mean, std = calculate_mean_std(distances)
            RMS, SD, CEP = cal_error(mean, std)
            print('The RMS is: ', RMS)
            print('The 2SD is: ', SD)
            print('The CEP is: ', CEP)
            break
        # input('Please input the test point: ')
        testpoint = []
        testpoint.append(input('Please input the test point longitude: ').split())
        testpoint.append(input('Please input the test point latitude: ').split())
        distance = CoordinateTransformation(benchmark, testpoint)
        distances.append(distance)