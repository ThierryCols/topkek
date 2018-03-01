from math import fabs
from operator import attrgetter
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

def get_distance_between(pos_a, pos_b):
    return get_distance(get_ride_between_rides(pos_a, pos_b))

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

def get_hash(d):
    return hash(frozenset(d.items()))

def build_hashtable(rides):
    hashes = list(map(get_hash, rides))
    return dict(zip(hashes, range(len(rides))))

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
            t += get_distance_between(ride, next_ride)

        # print('Ride', ride, 'gave score', ride_score)
        score += ride_score

    return score

def get_score(assignation, rides, parameters):
    return sum(get_vehicle_score(vehicle_assignation, rides, parameters) for vehicle_assignation in assignation)


def valid_rides_func(t, ride, vehicle_pos):
    return (t + get_distance(ride)) + get_distance_between(vehicle_pos, ride)


def optimization_func(t, ride, vehicle_pos):
    return get_distance_between(vehicle_pos, ride)


def choose_ride(t, rides, vehicle_pos):
    filtered_rides = list(filter(
        lambda ride: ride['latest_finish'] >= valid_rides_func(t, ride, vehicle_pos),
        rides
    ))
    if filtered_rides == []:
        return None
    greedy_ride = min(filtered_rides, key=lambda ride: optimization_func(t, ride, vehicle_pos))
    return greedy_ride


def do_ride(t, vehicle_position, ride):
    t += get_distance_between(vehicle_position, ride)
    t = max(ride['earliest_start'], t)
    t += get_distance(ride)
    vehicle_position = ride
    return t, vehicle_position


def output_assignations(assignations):
    with open(filename + '.out', 'w+') as f:
        string_assignations = []
        for rides in assignations:
            string_assignations.append(' '.join([str(_) for _ in [len(rides), *rides]]) + '\n')
        f.writelines(string_assignations)


#### Check that everything is valid for example a

with open('a_example.in') as f:
    lines = f.readlines()

parameters = parse_params(lines[0])
rides = parse_rides(lines[1:])

pp.pprint(parameters)
pp.pprint(rides)

assignation = [
    [0],     # 1
    [2, 1]   # 2
]

score = get_score(assignation, rides, parameters)
assert score == 10

# Optimization program bitch on a real example yeah

filename = 'b_should_be_easy'

with open(filename + '.in') as f:
    lines = f.readlines()

parameters = parse_params(lines[0])
rides = parse_rides(lines[1:])

rides_hashtable = build_hashtable(rides)

print()

available_rides = rides[:]

assignations = [[] for _ in range(parameters['vehicles'])]

vehicle_positions = [{
    'row_finish': 0,
    'col_finish': 0,
} for _ in range(parameters['vehicles'])]
vehicle_t = [0] * parameters['vehicles']

for vehicle in range(parameters['vehicles']):
    # print('Vehicle', vehicle)

    chosen_ride = choose_ride(vehicle_t[vehicle], available_rides, vehicle_positions[vehicle])

    while chosen_ride is not None and vehicle_t[vehicle] < parameters['time']:
        # Add ride to assignations
        assignations[vehicle].append(rides_hashtable[get_hash(chosen_ride)])

        available_rides = list(filter(lambda ride: ride != chosen_ride, available_rides))
        pp.pprint(chosen_ride)
        (vehicle_t[vehicle], vehicle_positions[vehicle]) = do_ride(vehicle_t[vehicle], vehicle_positions[vehicle], chosen_ride)
        # print('new t', vehicle_t[vehicle], 'vehicle position', vehicle_positions[vehicle])
        chosen_ride = choose_ride(vehicle_t[vehicle], available_rides, vehicle_positions[vehicle])

print(get_score(assignations, rides, parameters))
if len(available_rides) == 0:
    print('Missing', len(available_rides), 'rides! Woohoooooooo')
else:
    print('Missing', len(available_rides), 'rides....... :\'(')

output_assignations(assignations)
