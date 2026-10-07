"""
Oefening 2: Sliding Puzzle (8-puzzle)
======================================
Implementeer de sliding puzzle en los hem op met BFS/DFS.
"""
import numpy as np
from collections import deque
class SlidingPuzzle:
    GRIDSIZE = 3
    EMPTY = 0

    GOAL = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    def __init__(self, game):
        self.Game = np.array(game)

    def possible_new_configurations(self):
        # TODO: geef alle nieuwe configuraties door het lege vakje te verschuiven
        plaats_nul = self.locate_empty()
        mogelijke_richtingen =  [(-1,0),(1,0),(0,-1),(0,1)]

        
        lijst_puzzels = []
        for rij, kolom in mogelijke_richtingen:
            nieuwe_rij = plaats_nul[0] + rij
            nieuwe_kolom = plaats_nul[1] + kolom

            if 0 <= nieuwe_rij < self.GRIDSIZE and 0<= nieuwe_kolom < self.GRIDSIZE:
                puzzel = self.duplicate()
                getal_swap = puzzel.Game[nieuwe_rij][nieuwe_kolom]
                puzzel.Game[nieuwe_rij][nieuwe_kolom] = 0
                puzzel.Game[plaats_nul[0]][plaats_nul[1]] = getal_swap
                lijst_puzzels.append(puzzel)
        return lijst_puzzels

    def locate_empty(self):
        for row in range(self.GRIDSIZE):
            for col in range(self.GRIDSIZE):
                if self.Game[row][col] == self.EMPTY:
                    return (row, col)
        raise Exception("Geen leeg vakje!")

    def manhattan_distance(self):
        # TODO: bereken de Manhattan-afstand tot de goal-configuratie
        
        totaal_cost = 0
        for rij in range(self.GRIDSIZE):
            for kolom in range(self.GRIDSIZE):
                getal = self.Game[rij][kolom]
                if getal !=0:
                    rij_orginal = (getal-1)//3
                    kolom_orginal = (getal-1)%3
                    cost = abs(rij_orginal - rij) + abs(kolom_orginal - kolom)
                    totaal_cost+=cost
        return totaal_cost

    def is_goal(self):
        return np.array_equal(self.Game, self.GOAL)

    def duplicate(self):
        return SlidingPuzzle([[self.Game[r][c] for c in range(self.GRIDSIZE)] for r in range(self.GRIDSIZE)])

    def log(self):
        print("---")
        for row in self.Game:
            print(", ".join(str(int(x)) for x in row))
        print("---")


def solve_puzzle(start_puzzle):
    # TODO: los de puzzel op met BFS
    
    if start_puzzle.is_goal():
        return start_puzzle
    frontier = deque([start_puzzle])
    visited = set([str(start_puzzle.Game)])
    pad = {}
    while len(frontier) > 0:
        huidige_puzzel = frontier.popleft()
        mogelijkheden = huidige_puzzel.possible_new_configurations()
        for puzzel in mogelijkheden:
            is_the_goal = puzzel.is_goal()
            if is_the_goal:
                defini_pad = [str(puzzel.Game)]
                vader = str(huidige_puzzel.Game)
                defini_pad.append(vader)
                while vader != str(start_puzzle.Game):
                    grootvader = pad[vader]
                    defini_pad.append(grootvader)
                    vader = grootvader
                    
                return defini_pad


            if str(puzzel.Game) not in visited:
                pad[str(puzzel.Game)] = str(huidige_puzzel.Game)
                visited.add(str(puzzel.Game))
                frontier.append(puzzel)
            
            
        


if __name__ == "__main__":
    game = [
        [1, 2, 3],
        [4, 5, 0],
        [7, 8, 6]
    ]
    puzzle = SlidingPuzzle(game)
    print("Startconfiguratie:")
    puzzle.log()

    oplossing = solve_puzzle(puzzle)
    print("Oplossing:", oplossing)