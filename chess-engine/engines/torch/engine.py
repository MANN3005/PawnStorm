import torch
from chess import Board
from model import ChessModel
from auxiliary_func import board_to_matrix
import pickle
import numpy as np

def set_input(board: Board):
    board_matrix = board_to_matrix(board)
    X_tensor = torch.tensor(board_matrix, dtype=torch.float32).unsqueeze(0)
    return X_tensor

with open("chess-engine/models/move_to_int", "rb") as file:
    move_to_int = pickle.load(file)

if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Using MPS (Metal) on MacBook M2")
elif torch.cuda.is_available():
    device = torch.device("cuda")
    print("Using CUDA")
else:
    device = torch.device("cpu")
    print("Using CPU")
print(f'Using device: {device}')
model = ChessModel(num_classes=len(move_to_int))
model.load_state_dict(torch.load("chess-engine/models/final_model.pth", map_location=device))
model.to(device)
model.eval()

int_to_move = {v: k for k, v in move_to_int.items()}

def predict_move(board):
    X_tensor = set_input(board).to(device)
    with torch.no_grad():
        logits = model(X_tensor)
    logits = logits.squeeze(0)
    probabilities = torch.softmax(logits, dim=0).cpu().numpy()
    legal_moves = list(board.legal_moves)
    legal_moves_uci = [move.uci() for move in legal_moves]
    sorted_indices = np.argsort(probabilities)[::-1]
    for move_index in sorted_indices:
        move = int_to_move[move_index]
        if move in legal_moves_uci:
            return move
    return None

def uci_loop():
    board = Board()

    while True:
        command = input("Enter command: ").strip()
        if command == "uci":
            print("id author YourName")
            print("option name Hash type spin default 128 min 1 max 131072")
            print("option name Threads type spin default 1 min 1 max 8")
            print("uciok")
        elif command == "ucinewgame":
            board = chess.Board()
            best_move = None
      
        elif command == "isready":
            print("readyok")
        elif command.startswith("position"):
            tokens = command.split()
            if 'startpos' in tokens:
                board = Board()
                moves_start_index = tokens.index('startpos') + 2
            elif 'fen' in tokens:
                fen_string = " ".join(tokens[1:7])
                board = Board(fen_string)
                moves_start_index = tokens.index('moves') + 1 if 'moves' in tokens else len(tokens)
            for move in tokens[moves_start_index:]:
                board.push_uci(move)
        elif command.startswith("go"):
            best_move = predict_move(board)
            if best_move:
                print(f"bestmove {best_move}")
            else:
                print("bestmove 0000")  
        elif command == "quit":
            print("Exiting MyChessEngine. Goodbye!")
            break
        else:
            print("Unknown command. Please try again or enter 'quit' to exit.")

if __name__ == "__main__":
    uci_loop()
