import copy
import math
from MancalaBoard import MancalaBoard
from game_AI_AI import Game

class playAI_AI:
    MAX = 1
    MIN = -1

    def __init__(self, game, maxDepth=5):
        self.game = game
        self.maxDepth = maxDepth
    
    def computerTurn(self, player):
        value, bestPit = self.MinimaxAlphaBetaPruning(
            self.game,
            player,
            self.maxDepth,
            -math.inf,
            math.inf
        )

        side = "computer-1" if player == self.MAX else "computer-2"
        print(f"{side} plays {bestPit} (value={value})")

        i=self.game.state.doMove(self.game.playerSide[
            "COMPUTER_1" if player == self.MAX else "COMPUTER_2"
        ], bestPit)

        return i

    def MinimaxAlphaBetaPruning(self, game, player, depth, alpha, beta):

        if game.gameOver() or depth == 1:
            return game.evaluate(), None

        if player == self.MAX:
            bestValue = -math.inf
            bestPit = None

            for pit in game.state.possibleMoves(game.playerSide["COMPUTER_1"]):
                child_game = copy.deepcopy(game)
                i=child_game.state.doMove(child_game.playerSide["COMPUTER_1"], pit)
                if i==1:
                    value, _ = self.MinimaxAlphaBetaPruning(
                        child_game, self.MAX, depth - 1, alpha, beta
                    )
                else:
                    value, _ = self.MinimaxAlphaBetaPruning(
                        child_game, self.MIN, depth - 1, alpha, beta
                    )

                if value > bestValue:
                    bestValue = value
                    bestPit = pit

                if bestValue >= beta:
                    break

                alpha = max(alpha, bestValue)

            return bestValue, bestPit

        else:
            bestValue = math.inf
            bestPit = None

            for pit in game.state.possibleMoves(game.playerSide["COMPUTER_2"]):
                child_game = copy.deepcopy(game)
                i=child_game.state.doMove(child_game.playerSide["COMPUTER_2"], pit)

                if i == 2:  # COMPUTER_2 rejoue
                    value, _ = self.MinimaxAlphaBetaPruning(
                        child_game, self.MIN, depth - 1, alpha, beta
                    )
                else:
                    value, _ = self.MinimaxAlphaBetaPruning(
                        child_game, self.MAX, depth - 1, alpha, beta
                    )


                if value < bestValue:
                    bestValue = value
                    bestPit = pit

                if bestValue <= alpha:
                    break

                beta = min(beta, bestValue)

            return bestValue, bestPit

    def play(self):
        current_player = self.MAX

        while not self.game.gameOver():
            self.game.state.display()
            i = self.computerTurn(current_player)

            # COMPUTER_1 rejoue
            if current_player == self.MAX and i == 1:
                current_player = self.MAX

            # COMPUTER_2 rejoue
            elif current_player == self.MIN and i == 2:
                current_player = self.MIN

            # sinon on alterne
            else:
                current_player *= -1

        self.game.state.display()
        winner, score = self.game.findWinner()
        print("Winner:", winner, "Score:", score)


# Création du plateau
board = MancalaBoard()

# Création du jeu (Computer vs Computer)
game = Game(board)

# Création du contrôleur AI vs AI
play = playAI_AI(game, maxDepth=4)
print("===== AI vs AI TEST =====")
play.play()
