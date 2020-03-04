import PyGnuplot as Gp

first = True
base = 0
file = open("ground_readings_altered.csv", "r")
x = []
y = []
for line in file.readlines():
    elements = line.split(";")
    if first:
        base = int(elements[0])
        first = False
    x.append((int(elements[0]) - base) / 1000000000)
    y.append(elements[1].replace(",", "."))

Gp.plot([x, y], "ground.dat")
