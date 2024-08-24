import torch
from chess import Board
from model import ChessModel  # Ensure this import is correct
from auxiliary_func import board_to_matrix  # Ensure this import is correct
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

class UCIEngine:
    def __init__(self, model, int_to_move, device):
        self.model = model
        self.int_to_move = int_to_move
        self.device = device
        self.chess_board = Board()

    def display_welcome_message(self):
        print("Welcome to MyChessEngine!")
        print("Commands:")
        print(" - 'uci': Initialize the UCI engine")
        print(" - 'isready': Check if the engine is ready")
        print(" - 'position [startpos | fen <FEN_STRING>] moves <MOVE_LIST>': Set up the board position")
        print(" - 'go': Let the engine predict the best move")
        print(" - 'quit': Exit the engine")

    def set_position(self, position_command):
        self.chess_board = Board()
        tokens = position_command.split()
        if 'startpos' in tokens:
            moves_start_index = tokens.index('startpos') + 2  
        elif 'fen' in tokens:
            fen_string = " ".join(tokens[2:8])
            self.chess_board.set_fen(fen_string)
            moves_start_index = tokens.index('moves') + 1 if 'moves' in tokens else len(tokens)
        else:
            return  

        for move in tokens[moves_start_index:]:
            self.chess_board.push_uci(move)

    def predict_move(self):
        X_tensor = set_input(self.chess_board).to(self.device)
        with torch.no_grad():
            logits = self.model(X_tensor)
        logits = logits.squeeze(0)
        probabilities = torch.softmax(logits, dim=0).cpu().numpy()
        legal_moves = list(self.chess_board.legal_moves)
        legal_moves_uci = [move.uci() for move in legal_moves]
        sorted_indices = np.argsort(probabilities)[::-1]
        for move_index in sorted_indices:
            move = self.int_to_move[move_index]
            if move in legal_moves_uci:
                return move
        return None

    def uci_loop(self):
        self.display_welcome_message()  # Display welcome message when the loop starts
        while True:
            command = input().strip()  # No need to prompt for input, just strip leading/trailing whitespace
            if command == "uci":
                self.handle_uci()
            elif command == "isready":
                print("readyok")
            elif command.startswith("position"):
                self.set_position(command)
            elif command.startswith("go"):
                best_move = self.predict_move()
                if best_move:
                    print(f"bestmove {best_move}")
                else:
                    print("bestmove 0000")  # In case no move is found
            elif command == "quit":
                print("Exiting MyChessEngine. Goodbye!")
                break
            else:
                print("Unknown command. Please try again or enter 'quit' to exit.")

    def handle_uci(self):
        print("id name MyChessEngine")
        print("id author YourName")
        print("uciok")

uci_engine = UCIEngine(model, int_to_move, device)
uci_engine.uci_loop()
