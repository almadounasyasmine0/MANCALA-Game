import copy

class Game:
    """
    Classe Game représentant un nœud dans l'arbre de recherche Minimax.
    Conforme à 100% aux spécifications du projet Mancala.
    """
    
    # Constantes pour identifier les joueurs dans l'algorithme Minimax
    COMPUTER = 1      # Joueur MAX dans Minimax (l'ordinateur)
    HUMAN = -1        # Joueur MIN dans Minimax (l'humain)
    
    def __init__(self, state, computer_is_player1=True):
        """
        Initialise un nœud de jeu.
        
        Args:
            state (MancalaBoard): Instance de la classe MancalaBoard
            computer_is_player1 (bool): Si True, l'ordinateur est player1
        """
        # Attribut REQUIS: représente l'état du jeu
        self.state = state
        
        # Attribut REQUIS: dictionnaire qui stocke les côtés des joueurs
        if computer_is_player1:
            self.playerSide = {
                self.COMPUTER: 'player1',
                self.HUMAN: 'player2'
            }
        else:
            self.playerSide = {
                self.COMPUTER: 'player2',
                self.HUMAN: 'player1'
            }
    
    def gameOver(self):
        """
        REQUIS: Vérifie si le jeu est terminé et collecte les graines restantes.
        
        Returns:
            bool: True si le jeu est terminé, False sinon
        """
        # Vérifie si player1 a encore des mouvements possibles
        player1_has_moves = len(self.state.possibleMoves('player1')) > 0
        
        # Vérifie si player2 a encore des mouvements possibles
        player2_has_moves = len(self.state.possibleMoves('player2')) > 0
        
        # Si les deux joueurs ont encore des mouvements, le jeu continue
        if player1_has_moves and player2_has_moves:
            return False
        
        # Si un joueur n'a plus de mouvements, le jeu est terminé
        # On collecte les graines restantes selon les règles
        
        # On suppose que MancalaBoard a un attribut 'board' (dictionnaire)
        if hasattr(self.state, 'board'):
            # Cas 1: Player1 n'a plus de graines
            if not player1_has_moves:
                # Collecte graines de player2
                pits_player2 = ['G', 'H', 'I', 'J', 'K', 'L']
                total = 0
                for pit in pits_player2:
                    total += self.state.board.get(pit, 0)
                    self.state.board[pit] = 0
                # Ajoute au grenier de player2
                self.state.board['Store2'] = self.state.board.get('Store2', 0) + total
            
            # Cas 2: Player2 n'a plus de graines
            elif not player2_has_moves:
                # Collecte graines de player1
                pits_player1 = ['A', 'B', 'C', 'D', 'E', 'F']
                total = 0
                for pit in pits_player1:
                    total += self.state.board.get(pit, 0)
                    self.state.board[pit] = 0
                # Ajoute au grenier de player1
                self.state.board['Store1'] = self.state.board.get('Store1', 0) + total
        
        return True
    
    def findWinner(self):
        """
        REQUIS: Détermine le gagnant de la partie et son score.
        
        Returns:
            tuple: (gagnant, différence_score)
        """
        # Vérifie d'abord si le jeu est terminé SANS appeler gameOver()
        player1_has_moves = len(self.state.possibleMoves('player1')) > 0
        player2_has_moves = len(self.state.possibleMoves('player2')) > 0
        
        # Si les deux joueurs ont encore des mouvements, pas de gagnant
        if player1_has_moves and player2_has_moves:
            return None, 0
        
        # Si le jeu est terminé, on doit collecter les graines restantes
        # Vérifie si les graines n'ont pas déjà été collectées
        if not player1_has_moves:
            # Vérifie si player2 a encore des graines non collectées
            player2_pits = ['G', 'H', 'I', 'J', 'K', 'L']
            if any(self.state.board.get(pit, 0) > 0 for pit in player2_pits):
                self.gameOver()  # Collecte les graines une seule fois
        elif not player2_has_moves:
            # Vérifie si player1 a encore des graines non collectées
            player1_pits = ['A', 'B', 'C', 'D', 'E', 'F']
            if any(self.state.board.get(pit, 0) > 0 for pit in player1_pits):
                self.gameOver()  # Collecte les graines une seule fois
        
        # Récupère les scores depuis le plateau
        if hasattr(self.state, 'board'):
            board = self.state.board
            store1_seeds = board.get('Store1', 0)
            store2_seeds = board.get('Store2', 0)
        else:
            # Fallback en cas d'absence de board
            store1_seeds = store2_seeds = 0
        
        # Détermine qui contrôle quel grenier
        if self.playerSide[self.COMPUTER] == 'player1':
            computer_score = store1_seeds
            human_score = store2_seeds
        else:
            computer_score = store2_seeds
            human_score = store1_seeds
        
        # Calcule la différence de score
        score_difference = computer_score - human_score
        
        # Détermine le gagnant
        if score_difference > 0:
            winner = "COMPUTER"
        elif score_difference < 0:
            winner = "HUMAN"
        else:
            winner = "DRAW"
        
        return winner, abs(score_difference)
    
    def evaluate(self):
        """
        REQUIS: Fonction d'évaluation pour l'algorithme Minimax.
        
        Returns:
            int: value(n) = nbSeedsStore(playerSide[COMPUTER]) 
                         - nbSeedsStore(playerSide[HUMAN])
        """
        # Récupère les scores depuis le plateau
        if hasattr(self.state, 'board'):
            board = self.state.board
            store1_seeds = board.get('Store1', 0)
            store2_seeds = board.get('Store2', 0)
        else:
            # Fallback pour les tests
            store1_seeds = store2_seeds = 0
        
        # Applique l'équation selon la configuration
        if self.playerSide[self.COMPUTER] == 'player1':
            # Ordinateur = player1 = Store1
            # Humain = player2 = Store2
            return store1_seeds - store2_seeds
        else:
            # Ordinateur = player2 = Store2
            # Humain = player1 = Store1
            return store2_seeds - store1_seeds
