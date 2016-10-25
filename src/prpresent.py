
import pygame
import os.path

from pygame.locals import *

def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', num
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Slide(pygame.sprite.Sprite):
    def __init__(self, i):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image(str(i) + ".png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 0, 0

class Present:
    def __init__(self, screen):
        self.screen = screen
        #Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        #Groups for sprites
        self.bgs = pygame.sprite.Group()
        #Caches
        self.slides = {}
    def setSlide(self, i):
        nslide = self.slides.get(i)
        if nslide == None:
            self.slides[i] = Slide(i)
            nslide = self.slides.get(i)
        self.bgs.empty()
        self.bgs.add(nslide)
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.bgs.draw(self.screen)
        pygame.display.flip()
