import pygame
from surface import Surface

class Checkpoint(Surface):
    def __init__(self,x,y, checkpoint_id):
        super().__init__(x,y)
        self.checkpoint_id = checkpoint_id
        self.color=(128,128,128)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50))