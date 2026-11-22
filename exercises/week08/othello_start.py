"""
Oefening: Mini Othello met Evaluatiefunctie & Minimax
=======================================================
"""
import random
import copy


class Othello:
    def __init__(self):
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.player = 'X'

    def print_board(self):
        horizontal_line = "+---+---+---+---+---+---+---+---+"
        print(horizontal_line)
        for row in self.board:
            print("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            print(horizontal_line)

    def initialize_board(self):
        self.board[3][3] = self.board[4][4] = "O"
        self.board[3][4] = self.board[4][3] = "X"

    def is_valid_move(self, row, col, player):
        if self.board[row][col] != " ":
            return False

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row, col
            r += dr
            c += dc
            if not (0 <= r < 8) or not (0 <= c < 8):
                continue
            if self.board[r][c] == self.opponent(player):
                r += dr
                c += dc
                while (0 <= r < 8) and (0 <= c < 8):
                    if self.board[r][c] == " ":
                        break
                    if self.board[r][c] == player:
                        return True
                    r += dr
                    c += dc
        return False

    def opponent(self, player):
        return "O" if player == "X" else "X"

    def change_player(self):
        self.player = self.opponent(self.player)

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col, player):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            self.board[row][col] = player
            for dr, dc in directions:
                r, c = row, col
                r += dr
                c += dc
                while (0 <= r < 8) and (0 <= c < 8):
                    if self.board[r][c] == " ":
                        break
                    if self.board[r][c] == player:
                        while (r != row) or (c != col):
                            r -= dr
                            c -= dc
                            self.board[r][c] = player
                        break
                    r += dr
                    c += dc

    def count_pieces(self):
        x_count = sum(row.count("X") for row in self.board)
        o_count = sum(row.count("O") for row in self.board)
        return x_count, o_count

    def valid_moves(self, player):
        return [(r, c) for r in range(8) for c in range(8)
                if self.is_valid_move(r, c, player)]

    def random_move(self):
        # TODO: kies een geldige zet
        moves = self.valid_moves(self.player)
        if len(moves)>0:
            random.shuffle(moves)
            return moves[0]
        return None

    def evaluate(self, player):
        # TODO: evaluatiefunctie (bijv. stukken + mobiliteit)
        x_count, o_count = self.count_pieces()
        totaalcount_x = x_count
        totaalcount_o = o_count

        totaalcount_x += len(self.valid_moves('X'))
        totaalcount_o += len(self.valid_moves('O'))
        if player == 'X':
            return totaalcount_x - totaalcount_o

        else:
            return totaalcount_o - totaalcount_x

    def minimax(self, depth, is_maximizing, player):
        # TODO: implementeer minimax (simuleer zetten op een kopie)
        if depth == 0 or (not self.valid_moves('X') and not self.valid_moves('O')):
            return self.evaluate(player)
        if is_maximizing:
            moves = self.valid_moves(player)
            if not moves:
                return self.minimax(depth - 1, False, player)

            best_score = -float('inf')
            for row, col in moves:
                kopie = copy.deepcopy(self)
                kopie.make_move(row, col, player)
                score = kopie.minimax(depth - 1, False, player)
                best_score = max(best_score, score)
            return best_score
        else:
            tegenstander = self.opponent(player)
            moves_tegen = self.valid_moves(tegenstander)
            if not moves_tegen:
                return self.minimax(depth - 1, True, player)
            best_score_tegen = float('inf')
            for row, col in moves_tegen:
                kopie = copy.deepcopy(self)
                kopie.make_move(row, col, tegenstander)
                score_tegen = kopie.minimax(depth - 1, True, player)
                best_score_tegen = min(best_score_tegen,score_tegen)
                
            return best_score_tegen


    def best_move(self, depth=3):
        # TODO: kies de beste zet via minimax
        beste_score = -float('inf')
        beste_move = None
        for row,col in self.valid_moves(self.player):
            kopie = copy.deepcopy(self)
            kopie.make_move(row,col,self.player)
            score = kopie.minimax(depth-1,False,self.player)
            if beste_score < score:
                beste_score = score
                beste_move = [row,col]

        return beste_move



def play():
    game = Othello()

    while True:
        game.print_board()
        x_count, o_count = game.count_pieces()
        print(f"X: {x_count}, O: {o_count}")

        if not game.valid_moves(game.player):
            print("Geen geldige zetten meer.")
            game.change_player()
            if not game.valid_moves(game.player):
                print("Game over.")
                break

        if game.player == 'X':
            # TODO: laat de computer spelen met best_move()
            move = game.best_move()
            game.make_move(move[0],move[1],'X')
        else:
            print("Geldige zetten voor O:", game.valid_moves('O'))
            while True:
                try:
                    row = int(input("Kies een rij (0-7): "))
                    col = int(input("Kies een kolom (0-7): "))
                except ValueError:
                    print("Typ alstublieft een geldig getal tussen 0 en 7.")
                    continue

                if 0 <= row < 8 and 0 <= col < 8 and game.is_valid_move(row, col, 'O'):
                    game.make_move(row, col, 'O')
                    break
                else:
                    print("Ongeldige zet, probeer opnieuw.")

        game.change_player()


if __name__ == "__main__":
    play()