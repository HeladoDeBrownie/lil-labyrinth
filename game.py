from labyrinth import NoExit

HINT_ABBREVIATIONS = '''\
Any direction can be abbreviated by entering just its first letter.'''

HINT_GOAL = '''\
This is the goal room! Type WIN to finish the game.'''

class Game:
    def __init__(self, labyrinth, hints=True):
        self.labyrinth = labyrinth
        self.hints = hints

    def play(self):
        current_room = self.labyrinth.start_room
        self.render_room(current_room)
        self.show_hint(HINT_ABBREVIATIONS)

        try:
            while True:
                try:
                    player_input = input('> ').lower()
                except EOFError:
                    print()
                    raise Quit

                if player_input == 'quit':
                    raise Quit
                elif player_input == 'win':
                    if current_room.goal:
                        print("You sit in the throne. You've won, but it has cost you everything.")
                        break
                    else:
                        print("This isn't the goal room.")
                else:
                    direction = self.labyrinth.parse_direction(player_input)

                    if direction is None:
                        print('What?')
                    else:
                        try:
                            current_room = current_room.get_exit(direction)
                            self.render_room(current_room)
                        except NoExit:
                            print("Can't go that way.")
        except Quit:
            print('Farewell, adventurer!')

    def show_hint(self, text):
        if self.hints:
            print('HINT:', text)

    def render_room(self, room):
        print(room.description)
        print('Exits:', ', '.join([direction.label for direction in room.exits.keys()]))

        if room.goal:
            self.show_hint(HINT_GOAL)

class Quit(Exception): pass
