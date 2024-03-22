import pygame
import math
from track import Track

MAX_ANGLE_VELOCITY = 0.05
MAX_ACCELERATION = 0.25

class Kart():  # Vous pouvez ajouter des classes parentes
    """
    Classe implementant l'affichage et la physique du kart dans le jeu
    """
    def __init__(self, controller):
        # Initialisation des variables du kart
        self.__x = 50  # Position initiale x
        self.__y = 50  # Position initiale y
        self.__theta = 0  # Orientation initiale
        self.__v = 0  # Vitesse initiale
        self.__a = 0  # Accélération initiale
        self.__omega = 0  # Vitesse angulaire initiale
        self.__has_finished = False  # Indique si le kart a terminé la course
        self.controller = controller  # Contrôleur pour le kart
        self.__friction = 0.02  # Coefficient de friction
        self.__checkpoint_x = 50  # Position x du prochain checkpoint
        self.__checkpoint_y = 50  # Position y du prochain checkpoint
        self.__checkpoint_theta = 0  # Orientation au prochain checkpoint
        self.__next_checkpoint_id = 0  # ID du prochain checkpoint
        self.__current_surface = []  # Surface actuelle sur laquelle se trouve le kart
      
    # Définition des getters et setters
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def theta(self):
        return self.__theta

    @theta.setter
    def theta(self, value):
        self.__theta = value
        
    @property
    def v(self):
        return self.__v

    @v.setter
    def v(self, value):
        self.__v = value
        
    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        self.__a = value
        
    @property
    def omega(self):
        return self.__omega

    @omega.setter
    def omega(self, value):
        self.__omega = value
        
    @property
    def has_finished(self):
        return self.__has_finished

    @has_finished.setter
    def has_finished(self, value):
        self.__has_finished = value
        
    @property
    def friction(self):
        return self.__friction
    
    @friction.setter
    def friction(self, value):
        self.__friction = value

    @property
    def checkpoint_x(self):
        return self.__checkpoint_x

    @checkpoint_x.setter
    def checkpoint_x(self, value):
        self.__checkpoint_x = value

    @property
    def checkpoint_y(self):
        return self.__checkpoint_y

    @checkpoint_y.setter
    def checkpoint_y(self, value):
        self.__checkpoint_y = value

    @property
    def checkpoint_theta(self):
        return self.__checkpoint_theta

    @checkpoint_theta.setter
    def checkpoint_theta(self, value):
        self.__checkpoint_theta = value

    @property
    def next_checkpoint_id(self):
        return self.__next_checkpoint_id

    @next_checkpoint_id.setter
    def next_checkpoint_id(self, value):
        self.__next_checkpoint_id = value

    @property
    def current_surface(self):
        return self.__current_surface

    @current_surface.setter
    def current_surface(self, value):
        self.__current_surface = value
        
        
    def reset(self, initial_position, initial_orientation):
        # Définition des getters et setters
        self.x, self.y = initial_position  
        self.theta = initial_orientation  
        self.v = 0                         
        self.a = 0                         
        self.omega = 0                     
        
    def forward(self):
        # Accélérer en avant
        self.a += MAX_ACCELERATION
    
    def backward(self):
        # Accélérer en arrière
        self.a += -MAX_ACCELERATION
    
    def turn_left(self):       
        # Tourner à gauche
        self.omega += -MAX_ANGLE_VELOCITY
        
    def turn_right(self):     
        # Tourner à droite
        self.omega += +MAX_ANGLE_VELOCITY
    
    def layout(self, string):
        # Analyser la disposition du circuit à partir d'une chaîne de caractères
        lines = string.split('\n')
        track_layout = []
        for line in lines:
            row = [char for char in line]
            track_layout.append(row)
        return track_layout
                
    def update_position(self, string, screen):
        # Mettre à jour la position du kart en fonction de la disposition du circuit
        
        track_layout = self.layout(string)  # Analyser la disposition du circuit à partir de la chaîne de caractères.
        track_width = len(track_layout[0]) * 50  # Calculer la largeur totale du circuit.
        track_height = len(track_layout) * 50  # Calculer la hauteur totale du circuit.
        
        # Si le kart sort du circuit, réinitialiser sa position au dernier checkpoint.
        if self.x < 0 or self.x > track_width or self.y < 0 or self.y > track_height:
            self.x = self.checkpoint_x  # Position x du dernier checkpoint.
            self.y = self.checkpoint_y  # Position y du dernier checkpoint.
            self.theta = self.checkpoint_theta  # Orientation au dernier checkpoint.
            self.v = 0  # Réinitialiser la vitesse.
            self.a = 0  # Réinitialiser l'accélération.
            self.omega = 0  # Réinitialiser la vitesse angulaire.
            return      
        
        else:    
            block_x = int(self.x / 50)  # Déterminer la position en blocs du kart sur l'axe X.
            block_y = int(self.y / 50)  # Déterminer la position en blocs du kart sur l'axe Y.
            self.current_surface = track_layout[block_y][block_x]  # Identifier la surface actuelle sous le kart.
            track_element = Track.char_to_track_element[self.current_surface]  # Obtenir l'élément de piste correspondant.
            
            # Gérer les différentes surfaces du circuit.
            if self.current_surface == 'L':
                # Si le kart est sur la lave, le remettre au dernier checkpoint.
                self.x = self.checkpoint_x
                self.y = self.checkpoint_y
                self.theta = self.checkpoint_theta
                self.v = 0
                self.a = 0
                self.omega = 0
                
            elif self.current_surface == 'B':
                # Si le kart est sur un boost, augmenter sa vitesse temporairement.
                self.theta += self.omega
                self.v = 25
                self.x += self.v * math.cos(self.theta)
                self.y += self.v * math.sin(self.theta)
                self.a = 0
                self.omega = 0
            
            elif self.current_surface == 'G':
                # Si le kart est sur l'herbe, appliquer une friction supplémentaire.
                self.friction = 0.2
                self.theta += self.omega
                a1 = self.a - self.friction * self.v * math.cos(self.omega)
                self.v = a1 + self.v * math.cos(self.omega)
                self.x += self.v * math.cos(self.theta)
                self.y += self.v * math.sin(self.theta)
                self.a = 0
                self.omega = 0
                self.friction = 0.02
            
            elif self.current_surface in ['C', 'D', 'E', 'F']:
                # Si le kart atteint un checkpoint, mettre à jour le prochain checkpoint.           
                self.theta += self.omega
                a1 = self.a - self.friction * self.v * math.cos(self.omega)
                self.v = a1 + self.v * math.cos(self.omega)
                self.x += self.v * math.cos(self.theta)
                self.y += self.v * math.sin(self.theta)
                self.a = 0
                self.omega = 0
                
                checkpoint_id = track_element['params'][0]
                
                if checkpoint_id != self.next_checkpoint_id:
                    pass
                elif checkpoint_id == self.next_checkpoint_id:
                    if checkpoint_id == 3:
                        self.has_finished = True
                    else:
                        self.checkpoint_x = self.x
                        self.checkpoint_y = self.y
                        self.checkpoint_theta = self.theta
                        self.next_checkpoint_id = checkpoint_id + 1
                
            else:
                # Appliquer la logique de déplacement standard pour toute autre surface.
                self.theta += self.omega
                a1 = self.a - self.friction * self.v * math.cos(self.omega)
                self.v = a1 + self.v * math.cos(self.omega)
                self.x += self.v * math.cos(self.theta)
                self.y += self.v * math.sin(self.theta)
                self.a = 0
                self.omega = 0
            
    
    def draw(self, screen):
        # Dessiner le kart sur l'écran
        
        triangle_size = 20
        point1 = (self.x + triangle_size * math.cos(self.theta),
                  self.y + triangle_size * math.sin(self.theta))     
        angle_offset = math.pi / 6
        point2 = (self.x + triangle_size * math.cos(self.theta + math.pi - angle_offset),
                  self.y + triangle_size * math.sin(self.theta + math.pi - angle_offset))
        point3 = (self.x + triangle_size * math.cos(self.theta + math.pi + angle_offset),
                  self.y + triangle_size * math.sin(self.theta + math.pi + angle_offset))
        pygame.draw.polygon(screen, (255, 255, 255), [point1, point2, point3])