import math

bins = []
t0 = 76.8999
ta = 25.506
k = 0.0002647
t_start = 1582791479295278800


def initialize():
    for y in range(256):
        bins.append([])
        for x in range(256):
            bins[y].append(0)


def increment(x, y):
    bins[y][x] = bins[y][x] + 1


def save():
    file = open("matrix.dat", "w")
    for y in range(len(bins)):
        bins.append([])
        for x in range(len(bins[y])):
            file.write("{} {} {}\n".format(x, y, bins[y][x]))
        file.write("\n")


def ground_truth(t):
    return ta + (t0 - ta) * math.exp(-k * t)


def thermistor_temp(reading):
    voltage = (reading / 4096) * 2
    return (voltage - 0.5) / 0.01


def bin_index(value):
    return int((value - 19) / (91 - 19) * 255)


# Populate bins and generate file
file = open("thermistor_readings.csv", "r")
initialize()
for line in file.readlines():
    elements = line.split(";")
    time_seconds = (int(elements[0]) - t_start) / 1000000000
    ground = ground_truth(time_seconds)
    thermistor = thermistor_temp(int(elements[1]))

    bin_y = bin_index(thermistor)
    bin_x = bin_index(ground)
    increment(bin_x, bin_y)

save()


def max_bin(row):
    for (i, value) in enumerate(reversed(row)):
        if value != 0:
            return 255 - i

    return None


def min_bin(row):
    for (i, value) in enumerate(row):
        if value != 0:
            return i

    return None


def avg_bin(r):
    count = 0
    accum = 0
    for (index, value) in enumerate(r):
        accum += index * value
        count += value
    return int(round(accum / count))


def bin_temp(index):
    low = (index/255)*72+19
    high = ((index+1)/255)*72+19
    return (low+high)/2


file = open("bounds.csv", "w")
for (i, row) in enumerate(bins):
    if min_bin(row) is None:
        continue

    file.write("{};{};{};{}\n".format(bin_temp(i),
                                      bin_temp(min_bin(row)),
                                      bin_temp(max_bin(row)),
                                      bin_temp(avg_bin(row))))
