import numpy as np

# Define as dimensões do tabuleiro
ROWS = 6
COLS = 7

class PopOutGame: # Classe para representar o estado do jogo PopOut
    def __init__(self): # Inicializa o tabuleiro e o jogador atual
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.current_player = 1  # 1 ou -1
    
    def copy(self): # Cria uma cópia do estado atual do jogo
        new_game = PopOutGame()
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        return new_game