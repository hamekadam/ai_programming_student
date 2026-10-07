"""
Oefening 3: Maze met DFS
=========================
Implementeer DFS om een weg door het maze te vinden.
"""
import numpy as np


class Maze:
    def __init__(self, size, start, end, walls):
        self.size = size
        self.start = start
        self.end = end
        self.maze = np.zeros(size, dtype=str)
        self.maze[:, :] = '.'
        self.maze[start] = 'S'
        self.maze[end] = 'E'
        for wall in walls:
            self.maze[wall] = '#'

    def valid_moves(self, current):
        # TODO: geef lijst van (rij,kolom)-coördinaten die geldig zijn
        mogelijkheden = [(-1,0),(1,0),(0,-1),(0,1)]
        eind_lijst = []
        for rij,kolom in mogelijkheden:
            move_rij = current[0] + rij
            move_kolom = current[1] + kolom
            if 0 <= move_rij < self.size[0] and 0 <= move_kolom < self.size[1] and self.maze[move_rij][move_kolom]!= "#":
                eind_lijst.append((move_rij,move_kolom))
        return eind_lijst

    def extract_path(self, stack):
        # TODO: haal het pad uit de stack van start tot end
        pass

    def print_maze(self):
        for row in self.maze:
            print(' '.join(row))


def find_path(maze):
    # TODO: implementeer DFS met een stack
    if maze.start == maze.end:
        return "zelfde start en end"
    
    frontier = [(maze.start, [maze.start])]
    visited = set([maze.start])
    while len(frontier) > 0:
        huidige_maze, route = frontier.pop()
        kinderen = maze.valid_moves(huidige_maze)
        for kind in kinderen:
            nieuwe_route = route + [kind]
            if kind == maze.end:
                return nieuwe_route, len(nieuwe_route)
            if kind not in visited:
                visited.add(kind)
                frontier.append((kind, nieuwe_route))


if __name__ == "__main__":
    maze_size = (10, 10)
    start_point = (0, 0)
    end_point = (9, 9)
    walls = [(2, 1), (2, 2), (2, 3), (4, 6), (6, 6), (7, 6), (8, 6),
             (4, 7), (4, 8), (2, 2), (5, 2), (6, 2), (4, 2), (3, 2),
             (8, 0), (9, 6), (1, 8), (2, 8), (6, 9), (7, 9),
             (3, 6), (3, 7), (4, 1), (5, 1)]

    my_maze = Maze(maze_size, start_point, end_point, walls)
    pad, stappen = find_path(my_maze)

    my_maze.print_maze()
    print("Pad:", pad)
    print("Stappen:", stappen)