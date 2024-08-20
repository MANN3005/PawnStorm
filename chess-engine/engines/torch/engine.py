import random
import torch
from chess import Board
from model import ChessModel
from auxiliary_func import board_to_matrix
import pickle
import numpy as np
import time

def set_input(board: Board):
    board_matrix = board_to_matrix(board)
    X_tensor = torch.tensor(board_matrix, dtype=torch.float32).unsqueeze(0)
    return X_tensor

with open("PawnStorm/chess-engine/models/move_to_int", "rb") as file:
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
model.load_state_dict(torch.load("PawnStorm/chess-engine/models/final_model.pth", map_location=device))
model.to(device)
model.eval()

int_to_move = {v: k for k, v in move_to_int.items()}

class Engine:
    def __init__(self, model, int_to_move, device):
        self.turn = 0 
        self.model = model
        self.int_to_move = int_to_move
        self.device = device
        self.chess_board = Board()

    def visualize_board(self):
        print(self.chess_board)

    def make_move(self, move):
        self.chess_board.push_uci(move)
        self.turn = 1 - self.turn

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

    def play(self):
        self.visualize_board()

        if self.turn == 0:  
            legal_moves = list(self.chess_board.legal_moves)
            first_move = random.choice(legal_moves).uci()
            print(f"Random first move: {first_move}")
            self.make_move(first_move)
            self.visualize_board()

        while not self.chess_board.is_game_over():
            self.whose_turn()
            predicted_move = self.predict_move()
            time.sleep(5)

            if predicted_move:
                print(f"Predicted move: {predicted_move}")
                self.make_move(predicted_move)
                self.visualize_board()
            else:
                print("No valid move predicted.")
                break

        print("Game Over")
        print("Result:", self.chess_board.result())

    def whose_turn(self):
        if self.turn:
            print("Black's turn")
        else:
            print("White's turn")

az = Engine(model, int_to_move, device)
az.play()

