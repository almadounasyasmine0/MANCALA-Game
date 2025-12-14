class Game:
    def __init__(self, state):
        
        self.state = state

        # Définition des camps
        self.playerSide = {
            "COMPUTER_1": 1,
            "COMPUTER_2": 2 
        }
    def gameOver(self):
        board = self.state.board

        p1_empty = all(board[p] == 0 for p in self.state.player1_pits)
        p2_empty = all(board[p] == 0 for p in self.state.player2_pits)

        if p1_empty or p2_empty:
            # Si player 1 est vide, player 2 récupère ses graines
            if p1_empty:
                for p in self.state.player2_pits:
                    board['stor2'] += board[p]
                    board[p] = 0

            # Si player 2 est vide, player 1 récupère ses graines
            if p2_empty:
                for p in self.state.player1_pits:
                    board['stor1'] += board[p]
                    board[p] = 0

            return True

        return False
    def findWinner(self):
        store1 = self.state.board['stor1']
        store2 = self.state.board['stor2']

        if store1 > store2:
            return ("Player 1", store1)
        elif store2 > store1:
            return ("Player 2", store2)
        else:
            return ("Draw", store1)
    def evaluate(self):
    
        return (
            self.state.board['stor1']
            - self.state.board['stor2']
        )
