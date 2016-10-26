
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

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('assets', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

"""Shamelessly stolen: http://www.pygame.org/pcr/transform_scale/"""
def aspect_scale(img, (bx, by)):
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by
    return pygame.transform.scale(img, (int(sx), int(sy)))

class Slide(pygame.sprite.Sprite):
    def __init__(self, i):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image(str(i) + ".png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        w, h = screen.get_size()
        self.image = aspect_scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.center = self.area.center

class Present:
    def __init__(self, screen):
        self.screen = screen
        #Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        #Groups for sprites
        self.bgs = pygame.sprite.Group()
        #Sound channels
        self.chan = pygame.mixer.find_channel()
        #Caches
        self.slides = {}
        self.sounds = {}
    def setSlide(self, i):
        nslide = self.slides.get(i)
        if nslide == None:
            self.slides[i] = Slide(i)
            nslide = self.slides.get(i)
        self.bgs.empty()
        self.bgs.add(nslide)
    def setSound(self, loc):
        s = self.sounds.get(loc)
        if s == None:
            self.sounds[loc] = load_sound(loc)
            s = self.sounds.get(loc)
        self.chan.play(s)
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.bgs.draw(self.screen)
        pygame.display.flip()
