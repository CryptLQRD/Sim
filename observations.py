from typing import List


class Observation(object):
    def __init__(self, timestamp, x, y):
        self.timestamp = timestamp
        self.x = x
        self.y = y

    def __str__(self):
        return 'Observation(timestamp={}, x={}, y={})'.format(self.timestamp, self.x, self.y)

    def __repr__(self):
        return str(self)


class ObservedMonster(object):
    def __init__(self, alg=None, moveTime=None, observations: List[Observation] = None): #speed=None
        self.alg = alg
        self.moveTime= moveTime #speed = speed
        self.observations = observations or list()


def addObservation(monsters: List[ObservedMonster], observation: Observation, index: int = -1): #add_observation
    # find the matching monster
    known_monster = index >= 0
    monster_index = index

    if known_monster:
        monsters[monster_index].observations.append(observation)
    else:
        monsters.append(ObservedMonster(observations=[observation]))

#def addObservation(monsters: List[ObservedMonster], observation: Observation, index: int = -1): #add_observation
    # find the matching monster
#    known_monster = index >= 0
#    monster_index = index

#    if known_monster:
#        monsters[monster_index].observations.append(observation)
#    else:
#        monsters.append(ObservedMonster(observations=[observation]))


def print_all_observations(monsters: List[ObservedMonster]):
    for monster in monsters:
        print('Monster with alg {} and moveTime {}'.format(monster.alg, monster.moveTime))
        for obs in monster.observations:
            print('> timestamp={} x={} y={}'.format(obs.timestamp, obs.x, obs.y))
        print()

def printObs(monsters: List[ObservedMonster], index): #add_observation
    monster_index = index
    print('Monster with alg {} and moveTime {}'.format(monsters[monster_index].alg, monsters[monster_index].moveTime))
    for obs in monsters[monster_index].observations:
        print('> timestamp={} x={} y={}'.format(obs.timestamp, obs.x, obs.y))
    print()


if __name__ == '__main__':
    monsters = []  # type: List[ObservedMonster]
    #ObservedMonster(1, 2, Observation(timestamp=1, x=3, y=5))
    addObservation(monsters, Observation(timestamp=1, x=3, y=5))
    addObservation(monsters, Observation(timestamp=1, x=9, y=9))
    addObservation(monsters, Observation(timestamp=2, x=4, y=5), index=0)
    addObservation(monsters, Observation(timestamp=2, x=9, y=7), index=1)
    addObservation(monsters, Observation(timestamp=3, x=5, y=5), index=0)

    print_all_observations(monsters)

    print(monsters[0].observations[1])

    monsters[0].observations[1].x = 90

    print(monsters[0].observations)
