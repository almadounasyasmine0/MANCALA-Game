import copy
import math

class Play:
    """
    Classe principale qui gère le déroulement d'une partie de Mancala.
    Contient les fonctions pour les tours humain et ordinateur,
    ainsi que l'algorithme Minimax avec élagage Alpha-Beta.
    """
    
    # Constantes pour les joueurs dans Minimax
    COMPUTER = 1    # MAX player
    HUMAN = -1      # MIN player
    
    def __init__(self, game, max_depth=5):
        self.game = game
        self.max_depth = max_depth
    
    def humanTurn(self):
        print("\n" + "="*50)
        print("TOUR DU JOUEUR HUMAIN")
        print("="*50)
        
        self.display_board()
        human_side = self.game.playerSide[self.HUMAN]
        possible_moves = self.game.state.possibleMoves(human_side)
        
        if not possible_moves:
            print("Aucun mouvement possible. Tour passé.")
            return not self.game.gameOver()
        
        print(f"Mouvements possibles: {possible_moves}")
        
        while True:
            try:
                choice = input("Choisissez un puits (ex: A, B, C...): ").strip().upper()
                if choice in possible_moves:
                    break
                else:
                    print(f"Mouvement invalide. Choisissez parmi: {possible_moves}")
            except:
                print("Entrée invalide. Réessayez.")
        
        print(f"\nVous jouez le puits {choice}...")
        extra_turn = self.game.state.doMove(human_side, choice)
        
        self.display_board()
        
        if self.game.gameOver():
            print("\n" + "="*50)
            print("PARTIE TERMINÉE!")
            self.display_final_score()
            return False
        
        if extra_turn:
            print(" Dernière graine dans votre grenier! Vous rejouez!")
            return self.humanTurn()
        
        return True
    
    def computerTurn(self):
        """Même que précédent - pas de changement nécessaire"""
        print("\n" + "="*50)
        print("TOUR DE L'ORDINATEUR")
        print("="*50)
        
        self.display_board()
        print("L'ordinateur réfléchit...")
        
        best_value, best_pit = self.MinimaxAlphaBetaPruning(
            self.game, 
            self.COMPUTER, 
            self.max_depth, 
            -math.inf, 
            math.inf
        )
        
        computer_side = self.game.playerSide[self.COMPUTER]
        print(f"L'ordinateur joue le puits {best_pit} (évaluation: {best_value})")
        extra_turn = self.game.state.doMove(computer_side, best_pit)
        
        self.display_board()
        
        if self.game.gameOver():
            print("\n" + "="*50)
            print("PARTIE TERMINÉE!")
            self.display_final_score()
            return False
        
        if extra_turn:
            print("Dernière graine dans le grenier de l'ordinateur! Il rejoue!")
            return self.computerTurn()
        
        return True
    
    def MinimaxAlphaBetaPruning(self, game, player, depth, alpha, beta):
        """
        Fonction EXACTEMENT comme le pseudo-code fourni.
        
        # game est une instance de la classe Game et player = MAX or MIN
        def MinimaxAlphaBetaPruning(game, player, depth, alpha, beta):
            if game.gameOver() or depth == 1:
                bestValue = game.evaluate()
                return bestValue, None
            if player == MAX:
                # ... code pour MAX ...
            else:
                # ... code pour MIN ...
        """
        # CONDITION D'ARRÊT EXACTEMENT comme le pseudo-code
        if game.gameOver() or depth == 1:  # <-- depth == 1, PAS 0
            bestValue = game.evaluate()
            return bestValue, None
        
        # MAX player (COMPUTER)
        if player == self.COMPUTER:
            bestValue = -math.inf
            bestPit = None
            
            # Récupère les mouvements possibles
            # Note: Utilise EXACTEMENT game.playerSide[player] comme dans le pseudo-code
            possible_moves = game.state.possibleMoves(game.playerSide[player])
            
            for pit in possible_moves:
                # Crée une copie profonde
                child_game = copy.deepcopy(game)  # copy(game) dans pseudo-code
                
                # Exécute le mouvement - syntaxe EXACTE comme pseudo-code
                child_game.state.doMove(game.playerSide[player], pit)
                
                # Appel récursif - paramètres EXACTS comme pseudo-code
                # Note: -player, pas self.HUMAN
                value, _ = self.MinimaxAlphaBetaPruning(
                    child_game, 
                    -player,           # <-- -player, PAS self.HUMAN
                    depth - 1, 
                    alpha, 
                    beta
                )
                
                # Met à jour la meilleure valeur
                if value > bestValue:
                    bestValue = value
                    bestPit = pit
                
                # Élagage Alpha-Beta - EXACT comme pseudo-code
                if bestValue >= beta:
                    break  # Coupure Beta
                
                if bestValue > alpha:
                    alpha = bestValue
            
            return bestValue, bestPit
        
        # MIN player (HUMAN)
        else:
            bestValue = math.inf
            bestPit = None
            
            # Récupère les mouvements possibles
            possible_moves = game.state.possibleMoves(game.playerSide[player])
            
            for pit in possible_moves:
                # Crée une copie profonde
                child_game = copy.deepcopy(game)
                
                # Exécute le mouvement
                child_game.state.doMove(game.playerSide[player], pit)
                
                # Appel récursif
                value, _ = self.MinimaxAlphaBetaPruning(
                    child_game, 
                    -player,           # <-- -player, PAS self.COMPUTER
                    depth - 1, 
                    alpha, 
                    beta
                )
                
                # Met à jour la meilleure valeur
                if value < bestValue:
                    bestValue = value
                    bestPit = pit
                
                # Élagage Alpha-Beta
                if bestValue <= alpha:
                    break  # Coupure Alpha
                
                if bestValue < beta:
                    beta = bestValue
            
            return bestValue, bestPit
    
    def display_board(self):
        """Version simplifiée pour éviter les erreurs"""
        print("\n=== PLATEAU ACTUEL ===")
        # Affiche simplement le dictionnaire
        if hasattr(self.game.state, 'board'):
            for key, value in sorted(self.game.state.board.items()):
                print(f"{key}: {value}")
        print("=====================\n")
    
    def display_final_score(self):
        """Affiche le résultat final"""
        winner, score_diff = self.game.findWinner()
        
        if winner == "COMPUTER":
            print(f" L'ORDINATEUR GAGNE avec {score_diff} graines d'avance!")
        elif winner == "HUMAN":
            print(f" L'HUMAIN GAGNE avec {score_diff} graines d'avance!")
        else:
            print(" MATCH NUL!")
    
    def start_game(self):
        """Lance le jeu"""
        print("="*60)
        print("MANCALA - Ordinateur vs Humain")
        print("="*60)
        
        game_continues = True
        current_turn = self.COMPUTER  # L'ordinateur commence par défaut
        
        while game_continues:
            if current_turn == self.HUMAN:
                game_continues = self.humanTurn()
                if game_continues:
                    current_turn = self.COMPUTER
            else:
                game_continues = self.computerTurn()
                if game_continues:
                    current_turn = self.HUMAN
        
        print("\nFin de la partie!")
