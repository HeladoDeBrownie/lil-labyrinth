#!/usr/bin/env python3
from argparse import ArgumentParser

from game import Game
from labyrinth import Labyrinth

HELP_FLAG_HELP = '''\
Show this help message instead of playing the game.'''

HELP_FLAG_NUMBER_OF_ROOMS = '''\
Specify the number of rooms in the labyrinth. The default is 100. There will always be at least a start room and a goal room regardless of the number entered.'''

HELP_FLAG_NO_HINTS = '''\
Don't show hint messages, such as noting when you can win the game.'''

if __name__ == '__main__':
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        '--help', '-h', '-?',
        action='help',
        help=HELP_FLAG_HELP,
    )

    parser.add_argument(
        '--number-of-rooms', '-n', '--room-count', '-c',
        type=int,
        default=100,
        help=HELP_FLAG_NUMBER_OF_ROOMS,
    )

    parser.add_argument(
        '--no-hints',
        dest='hints',
        action='store_false',
        help=HELP_FLAG_NO_HINTS,
    )

    args = parser.parse_args()
    Game(Labyrinth(args.number_of_rooms), hints=args.hints).play()
