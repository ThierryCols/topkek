from math import fabs
import pprint

pp = pprint.PrettyPrinter(indent=4)

def parse_params(params_string):
    params_keys = ('rows', 'cols', 'vehicles', 'rides', 'bonus', 'time')
    params_values = map(lambda x: int(x.strip()), params_string.split(' '))
    return dict(zip(params_keys, params_values))

def parse_ride(ride_string):
    ride_keys = ('row_start', 'col_start', 'row_finish', 'col_finish', 'earliest_start', 'latest_finish')
    ride_values = map(lambda x: int(x.strip()), ride_string.split(' '))
    return dict(zip(ride_keys, ride_values))

def parse_rides(rides_string):
    return list(map(parse_ride, rides_string))

with open('a_example.in') as f:
    lines = f.readlines()

parameters = parse_params(lines[0])
rides = parse_rides(lines[1:])

assignation = [
    [0],     # 1
    [2, 1]   # 2
]

def get_distance(ride):
    return fabs(ride['row_start'] - ride['row_finish']) + fabs(ride['col_start'] - ride['col_finish'])

assert get_distance({   'col_finish': 3,
        'col_start': 0,
        'earliest_start': 2,
        'latest_finish': 9,
        'row_finish': 1,
        'row_start': 0}) == 4
assert get_distance({   'col_finish': 0,
        'col_start': 2,
        'earliest_start': 0,
        'latest_finish': 9,
        'row_finish': 1,
        'row_start': 1}) == 2

def get_ride_between_rides(ride_a, ride_b):
    ride_between = {
        'row_start': ride_a['row_finish'],
        'col_start': ride_a['col_finish'],
        'row_finish': ride_b['row_start'],
        'col_finish': ride_b['col_start'],
    }
    return ride_between

def get_vehicle_score(vehicle_assignation, rides, parameters):
    position = (0, 0)
    t = 0
    score = 0

    if vehicle_assignation == []:
        return 0

    # Go to the first ride
    ride_between = get_ride_between_rides({
        'row_finish': 0,
        'col_finish': 0,
    }, rides[vehicle_assignation[0]])
    t += get_distance(ride_between)

    for ride_idx, next_ride_idx in zip(vehicle_assignation, vehicle_assignation[1:] + [None]):
        ride = rides[ride_idx]
        ride_score = 0

        # Get bonus for arriving on time, yay
        if t <= ride['earliest_start']:
            t = ride['earliest_start']
            ride_score += parameters['bonus']

        # Do the ride
        distance = get_distance(ride)
        t += distance

        # Early arrival, you get the score
        if t <= ride['latest_finish']:
            ride_score += distance

        # Move to the next ride
        if next_ride_idx is not None:
            next_ride = rides[next_ride_idx]
            ride_between = get_ride_between_rides(ride, next_ride)
            t += get_distance(ride_between)

        print('Ride', ride, 'gave score', ride_score)
        score += ride_score

    return score

def get_score(assignation, rides, parameters):
    return sum(get_vehicle_score(vehicle_assignation, rides, parameters) for vehicle_assignation in assignation)


pp.pprint(parameters)
pp.pprint(rides)

score = get_score(assignation, rides, parameters)

print(score)
