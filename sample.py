class engine:
    # this will contain 2 things :- 1) boolean whoseTurn 2) board
    pass
    def __init__(self):
        self.turn = 0
        self.board = []
        l = ['r','n','b','q','k','b','n','r']
        self.board.append(l)
        l = ['p','p','p','p','p','p','p','p']
        self.board.append(l)
        for i in range(4):
            l2 = [' ',' ',' ',' ',' ',' ',' ',' ']
            self.board.append(l2)
        l = ['P','P','P','P','P','P','P','P']
        self.board.append(l)
        l = ['R','N','B','Q','K','B','N','R']
        self.board.append(l)
    
    def get_board(self):
        return self.board

    def get_board_visual(self):
        arr = self.board
        print("+---+---+---+---+---+---+---+---+")
        for i in range(8):
            # print(arr[i])
            for j in range(8):
                print( "| "+str(arr[i][j]),end=" ")
            print("| "+str(8-i))
            print("+---+---+---+---+---+---+---+---+")
        print("  a   b   c   d   e   f   g   h")


    def whose_turn(self):
        if self.turn:
            print("Black")
        else:
            print("White")
    def make_moves(self, arr):
        new_board = [row[:] for row in self.board]
        for l in arr:
            a = ord(l[0])-ord('a')
            b = ord(l[1])-ord('0')
            c = ord(l[2])-ord('a')
            d = ord(l[3])-ord('0')
            new_board[8-d][c] = new_board[8-b][a]
            new_board[8-b][a] = " "
        
        self.board = new_board



az = engine()
az.get_board_visual()
az.make_moves(["e2e4","e7e5"])
az.get_board_visual()