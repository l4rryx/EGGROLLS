import sys
import os
import subprocess
import time

def main():
    """Starting the game, by passing 2 arguments in the terminal"""
    if len(sys.argv) < 2:
        print('The game requires a filename to start.', file=sys.stderr)
        return
    with open(sys.argv[1], encoding='utf-8') as f:
        row = int(f.readline())
        moves = int(f.readline())
        level = [f.readline() for i in range(row)]
        clear_screen()
        print(*level)
        stats_and_input(moves, '', 0, level)

def stats_and_input(moves, prev_moves, curr_points, level):
    """
    This function serves as the inputter of the moves done by the player.
    It also keeps track of the statistics needed.
    This includes the remaining moves, previous moves done, and their current points.
    It also has the level which will be accessed by other functions.
    """

    def get_input():
        directions = input("Enter Move/s: ")
        _directions = []
        for letter in directions:
            if letter.upper() in {'L', 'R', 'F', 'B'}:
                _directions.append(letter.upper())
        movers(_directions, level, curr_points, moves, prev_moves)

    print(f"""Previous Moves: {prev_moves}\nMoves: {moves}\nPoints: {curr_points}""")
    if game_ender(level, moves):
        return
    else:
        get_input()


def movers(_directions, level, points, moves, directions):
    DIRECTION = {'L':(0, -1), 'R':(0, 1), 'F':(-1, 0), 'B': (1, 0)}
    PREV_MOVE = {'L':'←', 'R':'→', 'F':'↑', 'B': '↓'}
    grid_map = _listify(level)
    for d in _directions:
        if moves - 1 < 0:
            stats_and_input(moves, directions, points, grid_map)
        else:
            moves -= 1
            ind = 0
            eggs = _find_eggs(grid_map, d)
            done_moving = [False for egg in eggs]
            while not all(done_moving):
                loc_of_eggs = _find_eggs(grid_map, d)
                for egg in loc_of_eggs:
                    [i, j] = egg
                    if grid_map[i + DIRECTION[d][0]][j + DIRECTION[d][1]] in {"🥚", "🪺"}: #path is either an egg or full nest
                        done_moving[ind] = True
                        ind += 1
                    elif grid_map[i + DIRECTION[d][0]][j + DIRECTION[d][1]] == "🪹": #path is egg nest
                        grid_map[i][j] = "🟩"
                        grid_map[i + DIRECTION[d][0]][j + DIRECTION[d][1]] = "🪺"
                        done_moving[ind] = True
                        ind += 1
                        points += 10 + 1 + moves
                    elif grid_map[i + DIRECTION[d][0]][j + DIRECTION[d][1]] == "🍳": #path is frying pan
                        grid_map[i][j] = "🟩"
                        done_moving[ind] = True
                        ind += 1
                        points -= 5
                    elif grid_map[i + DIRECTION[d][0]][j + DIRECTION[d][1]] == "🟩": #path is not the wall
                        grid_map[i][j] = "🟩"
                        grid_map[i + DIRECTION[d][0]][j + DIRECTION[d][1]] = "🥚"
                    else: #meaning katabi na niya yung wall:
                        done_moving[ind] = True
                        ind += 1
                clear_screen()
                for row in grid_map:
                    print(''.join(row))
                time.sleep(0.5)
            directions += PREV_MOVE[d]
    stats_and_input(moves, directions, points, grid_map)


def _listify(level):
    """
    It makes the level a whole list, with every row being a list itself.
    """
    grid = []
    for row in level:
        rowed = []
        for col in row:
            rowed.append(col)
        grid.append(rowed)
    return grid 

def _find_eggs(grid, d):
    """
    Gives the coordinates of the eggs inside the grid. Additionally,
    the eggs get sorted based on priority (which egg is supposed to move
    first, which will be helpful in the other function).
    """
    coor = []
    DIRECTION_EGG = {'L':(1, 1), 'R':(1, -1), 'F':(1, 1), 'B':(-1, 1)}
    row = len(grid)
    col = len(grid[0])
    for i in range(row)[::DIRECTION_EGG[d][0]]:
        for j in range(col)[::DIRECTION_EGG[d][1]]:
            if grid[i][j] == '🥚':
                coor.append((i, j))
    return coor

def _find_emptynest(grid):
    """
    Gives the coordinates of the eggs inside the grid.
    """
    for row in grid:
        if '🪹' in row:
            return False
    return True

def _find_egg(grid):
    """
    Gives the coordinates of the eggs inside the grid.
    """
    for row in grid:
        if '🥚' in row:
            return False
    return True

def game_ender(grid, moves):
    if _find_emptynest(grid) or _find_egg(grid) or moves < 0:
        return True
    else:
        return False


def clear_screen():
    """Clears the terminal screen, if any"""
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run([clear_cmd])



main()
