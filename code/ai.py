import math
import pygame
import heapq

MAX_ANGLE_VELOCITY = 0.05
BLOCK_SIZE = 50

class AI():

    def __init__(self, layout_string):       
        self.__kart = None
        self.__track_layout = layout_string.split("\n")
        self.__checkpoints = []
        self.__need_update = True  # Indique si le chemin doit être recalculé
        self.__num = 0  # Numéro de point sur le chemin
        self.__point = (2, 2)  # Point de départ

    @property
    def kart(self):
        return self.__kart

    @kart.setter
    def kart(self, value):
        self.__kart = value

    @property
    def track_layout(self):
        return self.__track_layout

    @track_layout.setter
    def track_layout(self, value):
        self.__track_layout = value.split("\n")

    @property
    def checkpoints(self):
        return self.__checkpoints

    @checkpoints.setter
    def checkpoints(self, value):
        self.__checkpoints = value

    @property
    def need_update(self):
        return self.__need_update

    @need_update.setter
    def need_update(self, value):
        self.__need_update = value

    @property
    def num(self):
        return self.__num

    @num.setter
    def num(self, value):
        self.__num = value

    @property
    def point(self):
        return self.__point

    @point.setter
    def point(self, value):
        self.__point = value


    def distance_rules(self, position, final):
        return abs(position[0] - final[0]) + abs(position[1] - final[1])
    
    # def distance_rules(self, position, final):
    # Distance euclidienne pour A*
    #     return math.sqrt((position[0] - final[0]) ** 2 + (position[1] - final[1]) ** 2)

    def check_around(self, position):
        # Obtenir les voisins d'une position donnée sur la piste
        directions = [(0, -1), (-1, -1), (0, 1), (-1, 1), (-1, 0), (1, 1), (1, 0), (1, -1)]
        neighbors = []
        x, y = position
        # Parcourir les directions possibles et ajouter les voisins valides
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.track_layout[0]) and 0 <= ny < len(self.track_layout):
                if self.track_layout[ny][nx] != 'L':
                    neighbors.append((nx, ny))
        return neighbors
    
    def distance(self, neighbor):
    # Calculer le coût pour se déplacer d'une position à une autre
        x, y = neighbor      
        # Coût selon le type de terrain
        if self.track_layout[y][x] == 'R':
            # 'R' pour la route : coût standard, représentant un déplacement facile sur la route.
            # Un coût moyen est utilisé pour représenter le déplacement standard.
            return 50
        if self.track_layout[y][x] == 'B':
            # 'B' pour le boost : coût réduit, représentant un déplacement plus rapide grâce au boost.
            # Un coût nul est utilisé pour encourager l'IA à choisir ces chemins pour aller plus vite.
            return 0
        elif self.track_layout[y][x] == 'G':
            # 'G' pour l'herbe : coût élevé, car l'herbe ralentit le kart.
            # Un coût plus élevé est utilisé pour refléter la difficulté de déplacement sur l'herbe.
            return 150
        elif self.track_layout[y][x] == 'L':
            # 'L' pour la lave : coût très élevé, car la lave est un obstacle majeur.
            # Un coût extrêmement élevé est utilisé pour dissuader l'IA de traverser la lave.
            return 100000000
        else:
            # Autres types de terrain : coût standard.
            # Utilisé pour les types de terrain inconnus ou standard.
            return 50

    def locate_checkpoint(self, checkpoint_char):
        y = 0
        for row in self.track_layout:  # Parcourir chaque ligne du layout
            x = 0
            for col in row:  # Parcourir chaque colonne de la ligne
                if col == checkpoint_char:
                    return (x, y)  # Retourner la position si le checkpoint est trouvé
                x += 1  # Augmenter l'indice de la colonne
            y += 1  # Augmenter l'indice de la ligne
        return None  # Retourner None si le checkpoint n'est pas trouvé


    def find_path(self, start_point, end_point):
    
        open_list = []  # Liste ouverte pour les noeuds à explorer.
        heapq.heappush(open_list, (0, start_point))  # Ajouter le point de départ avec un score de 0.
        previous_nodes = {}  # Dictionnaire pour retracer le chemin.
        cost_from_start = {start_point: 0}  # Coût du point de départ jusqu'au noeud actuel.
        total_cost = {start_point: self.distance_rules(start_point, end_point)}  # Coût total estimé du chemin.
        # Boucle tant qu'il y a des noeuds à explorer.
        while open_list:
            current_node = heapq.heappop(open_list)[1]  # Prendre le noeud avec le coût total le plus bas.
            
            # Si le point d'arrivée est atteint, reconstruire et retourner le chemin.
            if current_node == end_point:
                path = []
                while current_node in previous_nodes:
                    path.append(current_node)
                    current_node = previous_nodes[current_node]
                path.append(start_point)  # Ajouter le point de départ à la fin du chemin.
                return path[::-1]  # Inverser le chemin pour avoir l'ordre du départ à l'arrivée.
            
            # Explorer les voisins du noeud actuel.
            for neighbor in self.check_around(current_node):
                # Calculer le score tentatif du noeud voisin.
                tentative_cost = cost_from_start[current_node] + self.distance(neighbor)
                # Si le score tentatif est inférieur, c'est un meilleur chemin, le sauvegarder.
                if tentative_cost < cost_from_start.get(neighbor, float('inf')):
                    previous_nodes[neighbor] = current_node
                    cost_from_start[neighbor] = tentative_cost
                    total_cost[neighbor] = tentative_cost + self.distance_rules(neighbor, end_point)
                    
                    # Ajouter le voisin à la liste ouverte s'il n'y est pas déjà.
                    if neighbor not in [n[1] for n in open_list]:
                        heapq.heappush(open_list, (total_cost[neighbor], neighbor))
        
        # Si le chemin n'est pas trouvé, retourner None.
        print("Aucun chemin trouvé")
        return None



    def calculate_complete_path(self):
    
        # Définir le point de départ en utilisant la position actuelle du kart.
        current_position = (int(self.kart.x // 50), int(self.kart.y // 50))
        # Initialiser la liste qui va contenir le chemin complet.
        complete_path = [current_position]
    
        # Itérer à travers tous les points de contrôle.
        for checkpoint in self.checkpoints:
            # Trouver la position du checkpoint sur la piste.
            checkpoint_position = self.locate_checkpoint(checkpoint)
            if checkpoint_position:
                # Trouver le chemin jusqu'à ce checkpoint.
                checkpoint_path = self.find_path(current_position, checkpoint_position)
                if checkpoint_path:
                    # Ajouter le chemin trouvé au chemin complet, en excluant le premier point pour éviter les doublons.
                    complete_path += checkpoint_path[1:]
                    # Mettre à jour la position actuelle pour le prochain itération.
                    current_position = checkpoint_position
    
        # Retourner le chemin complet.
        return complete_path

    def move(self, string):
        """
        Cette methode contient une implementation d'IA tres basique.
        L'IA identifie la position du prochain checkpoint et se dirige dans sa direction.

        :param string: La chaine de caractere decrivant le circuit
        :param screen: L'affichage du jeu
        :param position: La position [x, y] actuelle du kartq
        :param angle: L'angle actuel du kart
        :param velocity: La vitesse [vx, vy] actuelle du kart
        :param next_checkpoint_id: Un entier indiquant le prochain checkpoint a atteindre
        :returns: un tableau de 4 boolean decrivant quelles touches [UP, DOWN, LEFT, RIGHT] activer
        """

        # =================================================
        # D'abord trouver la position du checkpoint
        # =================================================     
        if not self.kart:
            return {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        if self.need_update:
            self.point = self.calculate_complete_path()
            self.need_update = True
        if self.kart.next_checkpoint_id == 0:
            self.checkpoints = ['C', 'D', 'E', 'F']
        if self.kart.next_checkpoint_id == 1:
            self.checkpoints = ['D', 'E', 'F']
        if self.kart.next_checkpoint_id == 2:
            self.checkpoints = ['E', 'F']
        if self.kart.next_checkpoint_id == 3:
            self.checkpoints = ['F']
            
        # On utilise x et y pour decrire les coordonnees dans la chaine de caractere
        # x indique le numero de colonne
        # y indique le numero de ligne    
        x, y = self.point[self.num]
        self.next_checkpoint_position = [x * BLOCK_SIZE + .5 * BLOCK_SIZE, y * BLOCK_SIZE + .5 * BLOCK_SIZE]
        if self.kart.x// 50 == x and self.kart.y // 50 == y:
            self.num += 1

        # =================================================
        # Ensuite, trouver l'angle vers le checkpoint
        # =================================================
        relative_x = self.next_checkpoint_position[0] - self.kart.x
        relative_y = self.next_checkpoint_position[1] - self.kart.y

        # On utilise la fonction arctangente pour calculer l'angle du vecteur [relative_x, relative_y]
        next_checkpoint_angle = math.atan2(relative_y, relative_x)

        # L'angle relatif correspond a la rotation que doit faire le kart pour se trouver face au checkpoint
        # On applique l'operation (a + pi) % (2*pi) - pi pour obtenir un angle entre -pi et pi
        relative_angle = (next_checkpoint_angle - self.kart.theta + math.pi) % (2 * math.pi) - math.pi

        # =================================================
        # Enfin, commander le kart en fonction de l'angle
        # =================================================
        
        if relative_angle > MAX_ANGLE_VELOCITY:
            # On tourne a droite
            command = [False, False, False, True]
        elif relative_angle < -MAX_ANGLE_VELOCITY:
            # On tourne a gauche
            command = [False, False, True, False]
        else:
            # On avance
            command = [True, False, False, False]

        key_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        keys = {key: command[i] for i, key in enumerate(key_list)}
        return keys