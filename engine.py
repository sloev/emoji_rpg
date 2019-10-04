def check_for_collisions(board, changes):
    for change in changes:
        old_position = change["old_position"]
        new_position = change["new_position"]
        incomming = change["sprite"]
        occupant = board[new_position["x"]][new_position["y"]]


def stand(data, initiator_emoji, current_path_x_y, target_path_x_y, target_emoji):
    source_z = list(data[current_path_x_y].itervalues())
    target_z = list(data[target_path_x_y].itervalues())

    source_z.remove(initiator_emoji)
    target_z.append(initiator_emoji)

    return {current_path_x_y: source_z, target_path_x_y: target_z}


ACTION_FUNCTIONS = {"stand": stand}


def make_move(data, current_path_x_y_z, target_path_x_y):
    """
    current_path is like:
        board.forrest.grid.0.0.0
        meaning
        board.specific_board.grid.x,y,z
    target_path lacks z:
        board.forrest.grid.0.0
    """
    current_path_x_y = current_path_x_y_z.rsplit(".", 1)[0]
    initiator_emoji = data[current_path_x_y_z]
    move_allowed = True
    patch = {}
    board = 1
    target_z = list(data[target_path_x_y].itervalues())
    action_path_prefix = (
        f"{target_path_x_y.rsplit('.', 3)[0]}.actions.{initiator_emoji}"
    )
    for target_emoji in reversed(target_z):
        target_path_x_y_z = f"{action_path_prefix}.{target_emoji}"
        action = data.get(target_path_x_y_z, None)
        if action:
            action_name = action["name"]
            action_func = ACTION_FUNCTIONS.get(action_name)
            if not action_func:
                raise KeyError(f"action func: '{action_name}'' does not exist")

            patch.update(
                action_func(
                    data,
                    initiator_emoji,
                    current_path_x_y,
                    target_path_x_y,
                    target_emoji,
                )
            )
    return patch


def apply_patch(data, patch):
    d = data.copy()
    for path, value in patch.items():
        d[path] = value
    return d

import curses, time

def run():
    """checking for keypress"""
    curses.wrapper(main)

def main(stdscr):

    def print_board(data, width, height):
        stdscr.clear()
        s = []
        for y in range(height):
            b = []
            for x in range(width):
                cell = data[f'boards.forrest.grid.{y}.{x}']
                z = sorted(cell.items(), key=lambda x: int(x[0]))
                index, emoji = z[-1]

                b.append(emoji)
            stdscr.addstr(''.join(b)+'\n')
        stdscr.refresh()
        # return curser to start position
        stdscr.move(0, 0)
    width, height = 20, 15
    data, player_x, player_y = create_game(width, height)
    new_x = player_x
    new_y = player_y
    print_board(data, width, height)
    stdscr.nodelay(1)  # do not wait for input when calling getch
    while True:  # making a loop
        key = stdscr.getch()
        if key == 119:
            new_y = max(0, min(player_y -1, height-1))
        elif key == 115:
            new_y = max(0, min(player_y +1, height-1))
        elif key == 100:
            new_x = max(0, min(player_x + 1, width-1))
        elif key == 97:
            new_x = max(0, min(player_x - 1, width-1))
        elif key == -1:
            pass
        else:
            break
        import json
        if new_y != player_y or new_x != player_x:
            patch = make_move(
                data,
                f"boards.forrest.grid.{player_y}.{player_x}.1",
                f"boards.forrest.grid.{new_y}.{new_x}"
                )
            data = apply_patch(data, patch)
            print_board(data, width, height)
            with open('out.json', 'w') as f:
                f.write(json.dumps(data.as_dict(), indent=2))
            player_x = new_x
            player_y = new_y



def create_game(width, height):
    import flatdict
    import random
    player = '😎'
    grass = '🌱'

    data = flatdict.FlatterDict(
        {
            "boards": {
                "forrest": {
                    "actions": {
                        "😎": {"🌱": {"name": "stand", "kwargs": {}}}
                    },
                    "grid":
                    {f'{y}':{f'{x}':[grass] for x in range(width)} for y in range(height)}
                }
            }
        },
        delimiter=".",
    )
    x,y = random.randint(0,width-1), random.randint(0,height-1)

    data[f"boards.forrest.grid.{y}.{x}"]["1"] = player
    return data, x,y


if __name__ == "__main__":
    run()
    #print(json.dumps(data.as_dict(), indent=2))


"""

flat = flatdict.FlatterDict({
    'boards': {
        'forrest':
            'actions': {
                '😂': {
                    '❤️' : {
                        'action_name':'take',
                        'action_kwargs': {
                        }
                    }
                },
            'grid': [
                [   # y=0
                    [   # x=0
                        '😂' # z=0
                    ],
                    [   # x=1
                        '❤️' # z=0
                    ]
                ]
            ]
        }
    },
    'actions': {
        'forrest':
        }
    }
}, delimiter='.')

its like this:
every emoji has an action towards another emoji if they colide.

The action can be many and always consist of
a function name
a list of kwargs


actions are defined as interactions between different emojis.
actions always have a defined initiator emoji and a target emoji:
ex:
    💩 is a player. there is a registered action for poop:
        💩 can move on grass and roads
        💩 can GO_INTO house
        💩 can GO_OUT_OF_DOOR

frontground: mostly text bubbles
background: everything else

there is a registry of moving characters and stationary characters.
moving characters are part of the update cycle and the move with a speed


maybe use deep patch :or deepmerge
https://stackoverflow.com/a/3233356/5324953

a cell in the grid consist of a z buffer stack:
when you walk on grass cells. you temporarily become a part of the cell with a higher z level index (append and pop)
the same when two players meet
"""
