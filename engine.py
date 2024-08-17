class engine:
    def __init__(self):
        self.turn = 0  
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
        a = ord(move[0]) - ord('a')
        b = ord(move[1]) - ord('1')
        c = ord(move[2]) - ord('a')
        d = ord(move[3]) - ord('1')
        self.board[7 - d][c] = self.board[7 - b][a]
        self.board[7 - b][a] = " "
        self.turn = 1 - self.turn  

   
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

az = engine()
az.play()
