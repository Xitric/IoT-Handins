file = open('measurements1.csv', 'r')
lines = file.readlines()

for i in range(int(len(lines) / 3)):
    before = int(lines[0 + i * 3].split(';')[2])
    after = int(lines[1 + i * 3].split(';')[2])
    receive = int(lines[2 + i * 3].split(';')[2])

    latency = receive - ((before + after) / 2)
    print(latency)
