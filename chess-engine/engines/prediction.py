from chess import Board, pgn
from auxiliary_func import board_to_matrix
import torch
from model import ChessModel

import pickle
import numpy as np

def set_input(board: Board):
    board_matrix = board_to_matrix(board)
    X_tensor = torch.tensor(board_matrix, dtype=torch.float32).unsqueeze(0)
    return X_tensor

with open("../../models/move_to_int", "rb") as file:
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
model.load_state_dict(torch.load("../../models/final_model.pth",  map_location=device))
model.to(device)
model.eval() 

int_to_move = {v: k for k, v in move_to_int.items()}
def predict_move(board: Board):
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



