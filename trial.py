# import chess
# board = chess.Board()
# # board.turn = chess.BLACK
# # print(chess.SQUARE_NAMES[5])
# # l = board.legal_moves
# # l2 = list(l)
# # for i in l2:
# #     board.push(i)
# #     print(board)
# #     board.pop()




# print(board)


import chess
# import chess.uci

def uci_loop():
    # engine = chess.uci.Engine()

    while True:
        line = input()
        if line == "uci":
            print("id name MyChessEngine")
            print("id author YourName")
            print("option name Hash type spin default 128 min 1 max 131072")
            print("option name Threads type spin default 1 min 1 max 8")
            print("uciok")
        elif line == "isready":
            print("readyok")
        elif line.startswith("setoption"):
            # Handle setoption commands
            pass
        elif line == "ucinewgame":
            # Reset the board and engine
            board = chess.Board()
            best_move = None
        elif line.startswith("position"):
            # Set the board position
            parts = line.split()
            if parts[1] == "startpos":
                board = chess.Board()
            elif parts[1] == "fen":
                board = chess.Board(parts[2])
            # else:
            #     raise ValueError("Unknown position command")
            for move in parts[3:]:
                board.push_uci(move)
        elif line.startswith("go"):
            # Make a move
            max_depth = 5
            best_move = engine(board, None, 1, max_depth)
            print("bestmove " + str(best_move))
        elif line == "quit":
            break
        else:
            raise ValueError("Unknown command")

def mateOpportunity(board, turn):
    if len(list(board.legal_moves)) == 0:
        return -9999 if turn == 0 else 9999
    return 0

def engine(board, candidate, depth, maxDepth):
    global best_move

    if depth == maxDepth or len(list(board.legal_moves)) == 0:
        return evaluation(board)
    
    move_list = list(board.legal_moves)
    move_list.sort(key=lambda move: move_ordering(board, move), reverse=True)

    if depth % 2 != 0:
        new_candidate = float("-inf")
    else:
        new_candidate = float("inf")
    
    for move in move_list:
        board.push(move)
        value = engine(board, new_candidate, depth + 1, maxDepth)

        if value > new_candidate and depth % 2 != 0:
            if depth == 1:
                best_move = move
            new_candidate = value
        elif value < new_candidate and depth % 2 == 0:
            new_candidate = value

        if candidate is not None and value < candidate and depth % 2 == 0:
            board.pop()
            break
        elif candidate is not None and value > candidate and depth % 2 != 0:
            board.pop()
            break

        board.pop()

    if depth > 1:
        return new_candidate
    else:
        return best_move

def evaluation(board):
    PV = {
        'pawn': 100,
        'knight': 320,
        'bishop': 330,
        'rook': 500,
        'queen': 950
    }
    DRAW_VALUE = 0

    if board.is_insufficient_material():
        return DRAW_VALUE

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))

    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))

    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))

    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))

    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    value = (
        PV['pawn'] * (wp - bp) +
        PV['knight'] * (wn - bn) +
        PV['bishop'] * (wb - bb) +
        PV['rook'] * (wr - br) +
        PV['queen'] * (wq - bq)
    )

    if board.turn == chess.WHITE:
        return value + mateOpportunity(board,0)
    return -value + mateOpportunity(board,1)

def move_ordering(board, move):
    if board.is_capture(move):
        return 10
    if board.is_check():
        return 5
    return 0

if __name__ == "__main__":
    uci_loop()