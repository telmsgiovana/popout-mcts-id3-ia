import numpy as np
from pyparsing import col
from pandas import col

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
    
    #Movimentos Possíveis
    def drop_piece(self, col): #Tenta colocar uma peça na coluna especificada
        for row in reversed(range(ROWS)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return True 
        return False #Coluna cheia, movimento inválido
    
    def pop_piece(self, col): #Tenta remover uma peça da coluna especificada
        if self.board[ROWS-1][col] == self.current_player:
            for row in range(ROWS-1, 0, -1):
                self.board[row][col] = self.board[row-1][col]
            self.board[0][col] = 0
            return True
        return False #Coluna vazia ou peça adversária, movimento inválido
    
    #Alternar Jogador
    def switch_player(self): #Alterna o jogador atual
        self.current_player *= -1

    #Gerar Jogadas Possíveis
    def get_valid_moves(self): #Gera uma lista de movimentos válidos (drop e pop) para o jogador atual
        moves = []

        # Drops
        for col in range(COLS): #Verifica se é possível colocar uma peça na coluna (se a parte superior da coluna estiver vazia)
            if self.board[0][col] == 0:
                moves.append(("drop", col))

        # Pops
        for col in range(COLS): #Verifica se é possível remover uma peça da coluna (se a parte inferior da coluna tiver uma peça do jogador atual)
            if self.board[ROWS-1][col] == self.current_player:
                moves.append(("pop", col))

        return moves
    
    #Visualização Simples (debug)
    def print_board(self): #Imprime o estado atual do tabuleiro
        print(np.flip(self.board, 0))