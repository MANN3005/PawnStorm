class engine:
    def __init__(self):
        self.turn = 0  # 0 for White, 1 for Black
        self.moves_list = []
        self.board = []
        l = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        self.board.append(l)
        l = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
        self.board.append(l)
        for i in range(4):
            l2 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            self.board.append(l2)
        l = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
        self.board.append(l)
        l = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        self.board.append(l)

    def get_board(self):
        return self.board

    def get_board_visual(self):
        arr = self.board
        print("+---+---+---+---+---+---+---+---+")
        for i in range(8):
            for j in range(8):
                print("| " + str(arr[i][j]), end=" ")
            print("| " + str(8 - i))
            print("+---+---+---+---+---+---+---+---+")
        print("  a   b   c   d   e   f   g   h")

    def whose_turn(self):
        if self.turn:
            print("Black's turn")
        else:
            print("White's turn")

    def make_move(self, move):
        self.moves_list.append(move)
        a = ord(move[0]) - ord('a')
        b = ord(move[1]) - ord('1')
        c = ord(move[2]) - ord('a')
        d = ord(move[3]) - ord('1')
        self.board[7 - d][c] = self.board[7 - b][a]
        self.board[7 - b][a] = " "
        self.turn = 1 - self.turn  # Toggle turn between 0 (White) and 1 (Black)

   
    def _convert_move(self, start_col, start_row, end_col, end_row):
        return chr(start_col + ord('a')) + str(8 - start_row) + chr(end_col + ord('a')) + str(8 - end_row)

    def play(self):
        self.get_board_visual()
        while True:
            self.whose_turn()
            print("Top moves:", self.get_top_move())
            move = input("Enter your move (e.g., e2e4): ")
            if move == "quit":
                print("Game ended.")
                break
            if len(move) == 4 and move[0] in 'abcdefgh' and move[2] in 'abcdefgh' and move[1] in '12345678' and move[3] in '12345678':
                self.make_move(move)
                self.get_board_visual()
            else:
                print("Invalid move. Please enter a valid move.")


    def is_move_legal(self, move):
    # Basic move validation
        if len(move) != 4:
            return False
        a = ord(move[0])-ord('a')
        b = ord(move[1])-ord('0')
        c = ord(move[2])-ord('a')
        d = ord(move[3])-ord('0')
        if a < 0 or a > 7 or b < 1 or b > 8 or c < 0 or c > 7 or d < 1 or d > 8:
            return False
        piece = self.board[8-b][a]
        if self.turn and piece.isupper():
            return False
        if not self.turn and piece.islower():
            return False

        # Check if the move is a valid move for the piece
        if piece == 'P' or piece == 'p':
            # Pawn
            if abs(b-d) == 1 and a == c:
                return True
            if b == 2 and d == 4 and a == c and self.board[8-3][a] == ' ':
                return True
            if b == 7 and d == 5 and a == c and self.board[8-6][a] == ' ':
                return True
            # En passant
            if abs(a-c) == 1 and abs(b-d) == 1 and self.board[8-d][c] == ' ':
                # Check if the opponent's pawn moved two squares on the previous move
                if self.turn and self.board[8-b][c] == 'p' and self.moves_list[-1] == self._convert_move(c, 7, c, 5):
                    return True
                if not self.turn and self.board[8-b][c] == 'P' and self.moves_list[-1] == self._convert_move(c, 2, c, 4):
                    return True
        elif piece == 'N' or piece == 'n':
            # Knight
            if abs(a-c) == 2 and abs(b-d) == 1:
                return True
            if abs(a-c) == 1 and abs(b-d) == 2:
                return True
        elif piece == 'B' or piece == 'b':
            # Bishop
            if abs(a-c) == abs(b-d):
                return True
        elif piece == 'R' or piece == 'r':
            # Rook
            if a == c or b == d:
                return True
        elif piece == 'Q' or piece == 'q':
            # Queen
            if a == c or b == d or abs(a-c) == abs(b-d):
                return True
        elif piece == 'K' or piece == 'k':
            # King
            if abs(a-c) <= 1 and abs(b-d) <= 1:
                return True

        return False

# To start the game:
az = engine()
az.play()
