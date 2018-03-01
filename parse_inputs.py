def parse_params(params_string):
    params_keys = ('rows', 'columns', 'vehicles', 'rides', 'bonus', 'time')
    params_values = map(lambda x: int(x.strip()), params_string.split(' '))
    return dict(zip(params_keys, params_values))

def parse_ride(ride_string):
    ride_keys = ('row_start', 'column_start', 'row_finish', 'column_finish', 'earliest_start', 'latest_finish')
    ride_values = map(lambda x: int(x.strip()), ride_string.split(' '))
    return dict(zip(ride_keys, ride_values))

def parse_rides(rides_string):
    return list(map(parse_ride, rides_string))

with open('a_example.in') as f:
    lines = f.readlines()

parameters = parse_params(lines[0])
rides = parse_rides(lines[1:])

print(parameters, rides)
