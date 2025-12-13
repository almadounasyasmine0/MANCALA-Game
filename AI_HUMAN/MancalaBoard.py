
class MancalaBoard :
    def __init__(self):
        self.board={
                        'A': 4,
                        'B': 4,
                        'C': 4,
                        'D': 4,
                        'E': 4,
                        'F': 4,
                        'G': 4,
                        'H': 4,
                        'I': 4,
                        'J': 4,
                        'K': 4,
                        'L': 4,
                        '1': 0,
                        '2': 0
                    }
        self.player1_pits=('A', 'B', 'C', 'D', 'E', 'F')
        self.player2_pits=('G', 'H', 'I', 'J', 'K', 'L')
        self.opposite_pits={
                        'A': 'G',
                        'B':' H',
                        'C': 'I',
                        'D': 'J',
                        'E': 'K',
                        'F': 'L',
                        'G': 'A',
                        'H': 'B',
                        'I': 'C',
                        'J': 'D',
                        'K': 'E',
                        'L': 'F'
                    }
        self.next_pit = {
                        'A': 'B',
                        'B': 'C',
                        'C': 'D',
                        'D': 'E',
                        'E': 'F', 
                        'F': 1,
                        1: 'L',
                        'L': 'K',
                        'K': 'J',
                        'J': 'I',
                        'I': 'H',
                        'H': 'G',
                        'G': 2,
                        2: 'A'
                        }

    pass

    def possibleMoves(self, player):
        if player == 1:
            return [p for p in self.player1_pits if self.board[p] > 0]
        else:
            return [p for p in self.player2_pits if self.board[p] > 0]


    def doMove(self, player, pit):

        seeds = self.board[pit] #nb of seeds 
        self.board[pit] = 0
        current = pit

        while seeds > 0:
            current = self.next_pit[current]

            # Ignorer le store adverse
            if player == 1 and current == 2:
                continue
            if player == 2 and current == 1:
                continue

            self.board[current] += 1
            seeds -= 1

        # Capture
        if player == 1 and current in self.player1_pits and self.board[current] == 1:
            opp = self.opposite[current]
            if self.board[opp] > 0:
                self.board[1] += self.board[opp] + 1
                self.board[current] = 0
                self.board[opp] = 0

        if player == 2 and current in self.player2_pits and self.board[current] == 1:
            opp = self.opposite[current]
            if self.board[opp] > 0:
                self.board[2] += self.board[opp] + 1
                self.board[current] = 0
                self.board[opp] = 0

        # Tour supplémentaire
        if (player == 1 and current == 1) or (player == 2 and current == 2):
            return player  # rejoue

        return 2 if player == 1 else 1
