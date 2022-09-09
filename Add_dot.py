'''
phase can just be 0 or 0.5 to define a square wave
'''
import datetime
from functools import reduce
DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}


def str2int(str):
    def char2num(s):
        return DIGITS[s]
    return reduce(lambda x, y: x*10+y, map(char2num, str))


#Create a square wave function to define the grayscale of the dots
def grayscale_dot1(phase):
    ISOTIMEFORMAT_F = '%f'
    f_time1 = datetime.datetime.now().strftime(ISOTIMEFORMAT_F)
    f_time2 = f_time1[:3]
    time_cal = str2int(f_time2) + phase
    if time_cal >= 1000:
        time_cal = time_cal - 1000
    if time_cal > 500:
        gray_parameter = 1
    else:
        gray_parameter = 0
    return gray_parameter
