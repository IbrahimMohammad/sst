#!/bin/python3

# estimated time, size and speed calculator

from math import modf,log

# when we leave days we lose some precision so we use average month
# and average year. the average is 30.4368499 days in a month
# because there are 365.242199 days in a year.
# this from google calculator:) so here is seconds_per_unit dict
s_p_u = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'M': 2629743.833,
        'y': 31556926,
        }

# diu exponent
expos = {
        'k': 1,
        'm': 2,
        'g': 3,
        't': 4,
        'p': 5,
        'e': 6,
        'z': 7,
        'y': 8,
        }

def diu_converter(num, unit):
    """ convert digital information units to bytes """
    # convert all letters in unit to lower case
    unit = unit.lower()
    # base number ib or b
    if unit[1] == 'i':
        # it is 1024
        base = 1024
    elif unit[1] == 'b':
        # it is 1000
        base = 1000
    else:
        # unkown unit
        print('Error: unkown unit')
        return False
    # get exponent
    exp = expos.get(unit[0])
    if exp == None:
        # unkown unit
        print("Error: unkown unit")
        return False
    # convert
    bytes = num * base ** exp
    return bytes, base


def is_input(inputs):
    """ is there are inputs? """
    if inputs:
        return True
    else:
        # no inputs
        print("Error: no inputs")
        return False


def good_len(itr, length, message):
    """ check inputs len """
    if len(itr) < length:
        # error less than required lenth
        print(message)
        return False
    return True


def time_converter(times):
    """ convert time to seconds """
    # split times in list of words
    times = times.split()
    # hold result
    total_seconds = 0
    # times is a list like this ['5h','3m','30s']
    for time in times:
        # check time len. 2 letters at least
        message = "Error: " + time + " is not a correct time."
        if not good_len(time, 2, message):
            return False
        # time unit is the last char in the string
        time_unit = time[-1]
        time_num = time[:-1]
        # is it a correct time?
        if not time_unit.isalpha() or not time_num.isnumeric():
            # error unkown time unit or number
            print("Error unkown time format in", time)
            return False
        # okay
        # convert to int for calculations
        time_num = int(time_num)
        # get how much sec in one of this unit
        sec_in_unit = s_p_u.get(time_unit)
        # is it known time unit?
        if sec_in_unit == None:
            # unkonwn time unit
            print("Error: unkown time unit", time_unit, "in", time)
            return False
        # convert time to seconds
        seconds = time_num * sec_in_unit
        # add current seconds to total_seconds
        total_seconds += seconds
    # after finsh the for loop return the result as int
    return int(total_seconds)


def unit_in_sec(unit, sec_in_unit, seconds):
    """ calculate how much unit in seconds """
    # convert seconds to unit
    sec_to_unit = seconds / sec_in_unit
    # split fraction and integer parts of sec_to_unit
    f_and_i = modf(sec_to_unit)
    # how much unit in seconds
    unit_in_seconds = int(f_and_i[1])
    # how much seconds left
    seconds = round(f_and_i[0] * sec_in_unit)
    return unit_in_seconds, seconds


def seconds_to_time(seconds):
    """ convert seconds to readable time """
    # this will hold the readable time
    time = ''
    # loop through units begin with the bigger unit
    for sec_in_unit in sorted(s_p_u.values(), reverse=True):
        # find the unit for the current sec_in_unit value
        unit = list(s_p_u.keys())[
                list(s_p_u.values()).index(sec_in_unit)
                ]
        # if seconds bigger than or equal to current unit seconds
        # then see how much of this unit do we have in seconds
        if seconds >= sec_in_unit:
            # calculate how much unit in the curent seconds
            unit_in_seconds, seconds = unit_in_sec(unit, sec_in_unit, seconds)
            # generate the time for this unit and add it to readable time
            time += str(unit_in_seconds) + unit + ' '
    # return the readable time string and strip the last space
    return time.rstrip()

def readable_diu(bytes, base):
    """ convert bytes to readable digital information unit """
    # get the exponent
    exp = int(log(bytes, base))
    # calc exact number
    readable_num = round(bytes / base ** exp, 2)
    # find the unit from the exponent value
    readable_unit = list(expos.keys())[
            list(expos.values()).index(exp)
            ]
    # ib or b ?
    if base == 1024:
        readable_unit += 'i'
    # bulid the readable digital information unit
    readable_diu = str(readable_num) + readable_unit + 'b'
    return readable_diu

"""
times = input("Please enter time: ")
if not is_input(times):
    exit(1)
seconds = time_converter(times)
if seconds:
    print("seconds =", seconds, '\n', seconds_to_time(seconds))
"""

diu = input("Please enter size: ")

# remove all spaces
diu = diu.replace(' ', '')
# is there are inputs?
if not is_input(diu):
    exit(1)
# check inputs len. 3 letters at least
if not good_len(diu, 3, "Error: too short input"):
    exit(1)

# get first char
first_cahr = 0
for i, char in enumerate(diu):
    if char.isalpha():
        # if the first char is alpha
        if i < 1:
            print("Error: the letter", char, "can't be first letter")
            exit(1)
        first_char = i
        break

# get num and unit
if first_char < 1:
    # error
    print("Error: no unit found")
    exit(1)
num = int(diu[:first_char])
unit = diu[first_char:]

# check unit it must be less than or equal 3 chars and last char is b
if len(unit) > 3 and unit[-1] != 'b':
    # unknow unit
    print("Error: unkown unit", unit)
    exit(1)

bytes, base = diu_converter(num, unit)
# check that bytes is not 0 and not false
if not bytes:
    exit(1)
print(bytes, '=', readable_diu(bytes, base))
