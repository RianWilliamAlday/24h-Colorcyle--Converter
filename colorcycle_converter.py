import sys

if len(sys.argv) <= 1:
    print("Usage: python colorcycle_converter.py <colorcycle.dat>")
    exit(0)

def parse_line(line):
    values = line.strip().split()
    return [float(v) for v in values[:12]]

def interpolate(l1, l2, f):
    return [round((1.0-f)*v1 + f*v2, 3) for v1, v2 in zip(l1, l2)]

def make24h(lines):
    w = []
    w.append(lines[0])  # midnight
    w.append(interpolate(lines[0], lines[1], 1.0/5.0))  # 1am
    w.append(interpolate(lines[0], lines[1], 2.0/5.0))  # 2am
    w.append(interpolate(lines[0], lines[1], 3.0/5.0))  # 3am
    w.append(interpolate(lines[0], lines[1], 4.0/5.0))  # 4am
    w.append(lines[1])  # 5am
    w.append(lines[2])  # 6am
    w.append(lines[3])  # 7am
    w.append(interpolate(lines[3], lines[4], 1.0/5.0))  # 8am
    w.append(interpolate(lines[3], lines[4], 2.0/5.0))  # 9am
    w.append(interpolate(lines[3], lines[4], 3.0/5.0))  # 10am
    w.append(interpolate(lines[3], lines[4], 4.0/5.0))  # 11am
    w.append(lines[4])  # midday
    w.append(interpolate(lines[4], lines[5], 1.0/7.0))  # 1pm
    w.append(interpolate(lines[4], lines[5], 2.0/7.0))  # 2pm
    w.append(interpolate(lines[4], lines[5], 3.0/7.0))  # 3pm
    w.append(interpolate(lines[4], lines[5], 4.0/7.0))  # 4pm
    w.append(interpolate(lines[4], lines[5], 5.0/7.0))  # 5pm
    w.append(interpolate(lines[4], lines[5], 6.0/7.0))  # 6pm
    w.append(lines[5])  # 7pm
    w.append(lines[6])  # 8pm
    w.append(interpolate(lines[6], lines[7], 1.0/2.0))  # 9pm
    w.append(lines[7])  # 10pm
    w.append(interpolate(lines[7], lines[0], 1.0/2.0))  # 11pm
    return w

def format_line(values):
    return " ".join([f"{v:.3f}" for v in values])

path = sys.argv[1]
with open(path, 'r') as f:
    lines = [parse_line(l) for l in f.readlines() if len(l.strip()) > 0]

num_weather = len(lines) // 8

newlines = []
for i in range(num_weather):
    weather_lines = lines[i*8:(i+1)*8]
    newlines += make24h(weather_lines)

remaining_start = num_weather * 8
if remaining_start < len(lines):
    newlines += lines[remaining_start:]

for i, line in enumerate(newlines):
    if i % 24 == 0 and i > 0:
        print()
    
    print(format_line(line))