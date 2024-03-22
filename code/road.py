import pygame
from surface import Surface
class Road(Surface):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color=(0,0,0)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50))