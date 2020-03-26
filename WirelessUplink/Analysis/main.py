from datetime import datetime

file = open('logs.csv', 'r')
date_format = '%Y-%m-%d %H:%M:%S.%f'
previous_send_time = None
previous_reception_time = None
start = None
out = open('result.csv', 'w')

out.write('send_diff;receive_diff\n')
for line in file:
    elements = line.split(';')
    number = elements[0]
    send = datetime.strptime(elements[1], date_format)
    receive = datetime.strptime(elements[2], date_format)
    latency = elements[3]
    temperature = elements[4]
    luminance = elements[5]

    if start is None:
        start = receive
    time_since_start = receive - start

    if previous_send_time is not None:
        send_diff = send - previous_send_time
        receive_diff = receive - previous_reception_time
        out.write('{};{};{}\n'.format(time_since_start.total_seconds(), send_diff.total_seconds(), receive_diff.total_seconds()))

    previous_send_time = send
    previous_reception_time = receive


