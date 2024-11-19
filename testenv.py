import simpy

def car(env):
    while True:
        print('Start parking at %d' % env.now)
        parkingDuration = 5
        yield env.timeout(parkingDuration)

        print('Start Driving at %d' % env.now)
        tripDuration = 2
        yield env.timeout(tripDuration)

env = simpy.Environment()
env.process(car(env))
env.run(until=15)