from random import choice

ROOM_DESCRIPTION_START = 'An inactive portal device is here. You came through it to get here.'
ROOM_DESCRIPTION_GOAL = "You're in a throne room where everything is made of gold."

ROOM_DESCRIPTIONS = [
    "You're along the edge of an endless abyss. Oh, wait, it's painted flat onto the ground.",
    "You're at a lavish feast. All of the food is made of plastic.",
    "You're at an underwater coral reef. Blub!",
    "You're in a cozy lounge. Did you just hear a friend's voice?",
    "You're in a graveyard. The wind is howling.",
    "You're in a hobbit hole, uninvited.",
    "You're in a jail. All the prisoners were freed ages ago.",
    "You're in a server room. Could it be running this place?",
    "You're in a throne room where everything is made of wood.",
    "You're inside of a gacha capsule.",
]

class Labyrinth:
    def __init__(self, room_count):
        self.directions = set()
        self.direction_aliases = {}
        self.add_direction_pair('north', 'n', 'south', 's', 0)
        self.add_direction_pair('east', 'e', 'west', 'w', 1)
        self.add_direction_pair('up', 'u', 'down', 'd', 2)
        self.add_direction_pair('ana', 'a', 'kata', 'k', 3)

        self.rooms = {} # 4D point → room

        # Place the start room.
        self.rooms[(0, 0, 0, 0)] = Room(ROOM_DESCRIPTION_START)

        for _ in range(room_count - 2):
            new_room = Room(choice(ROOM_DESCRIPTIONS))
            while not self.try_to_place(new_room): pass

        goal_room = Room(ROOM_DESCRIPTION_GOAL, goal=True)
        while not self.try_to_place(goal_room): pass

    def add_direction_pair(self, label_a, short_a, label_b, short_b, dimension):
        (direction_a, direction_b) = Direction.make_pair(label_a, label_b, dimension)
        self.directions.add(direction_a)
        self.directions.add(direction_b)
        self.direction_aliases[label_a] = self.direction_aliases[short_a] = direction_a
        self.direction_aliases[label_b] = self.direction_aliases[short_b] = direction_b

    def try_to_place(self, new_room):
        (coordinates, old_room) = choice(list(self.rooms.items()))
        direction = choice(list(self.directions))
        new_coordinates = list(coordinates)
        new_coordinates[direction.dimension] += direction.polarity
        new_coordinates = tuple(new_coordinates)

        # Is the tile occupied?
        if self.rooms.get(new_coordinates) is None:
            # It's unoccupied; place the new room.
            self.rooms[new_coordinates] = new_room
            old_room.dig(direction, new_room)
            return True
        else:
            # it's occupied; create a new connection anyway.
            old_room.dig(direction, self.rooms[new_coordinates])
            return False

    @property
    def start_room(self):
        return self.rooms[(0, 0, 0, 0)]

    def parse_direction(self, string):
        return self.direction_aliases.get(string, None)

class Room:
    def __init__(self, description, goal=False):
        self.description = description
        self.goal = goal
        self.exits = {}

    def add_exit(self, direction, destination):
        self.exits[direction] = destination

    def get_exit(self, direction):
        try:
            return self.exits[direction]
        except KeyError:
            raise NoExit

    def dig(self, direction, destination):
        self.exits[direction] = destination
        destination.exits[direction.opposite] = self

class Direction:
    def __init__(self, label, dimension, polarity, opposite=None):
        self.label = label
        self.dimension = dimension
        self.polarity = polarity
        self.opposite = opposite

    @staticmethod
    def make_pair(label_a, label_b, dimension):
        direction_a = Direction(label_a, dimension, -1, None)
        direction_b = Direction(label_b, dimension, +1, direction_a)
        direction_a.opposite = direction_b
        return (direction_a, direction_b)

class NoExit(Exception): pass
