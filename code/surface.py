from abc import ABC,abstractmethod

# First, define the abstract Surface class
class Surface(ABC):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.color=(0,0,0)
        
    @abstractmethod    
    def draw(self, screen):
        pass