
#Import Modules
import os, pygame
import os.path
from zipfile import ZipFile


from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from prutil import *
from prsound import *
from prpresent import *


def setup():
    setupDir("assets")

def addCmd(cmds, frame, s):
    cmd = cmds.get(frame)
    if cmd == None:
        cmds[frame] = []
        cmd = cmds.get(frame)
    cmd.append(s.split())

def extractSlides(name):
    extractHere(name + "_rec.zip")
    extractDir("assets.zip", 'assets')
    cmds = {}
    frame = 0
    lines = [line.rstrip('\n') for line in open('pres.txt')]
    for line in lines:
        if line[-1] == ':':
            frame = int(line[:-1])
        else:
            addCmd(cmds, frame, line)
    return cmds

def execute(exe, pres):
    ret = True
    if exe == None:
        return ret
    for c in exe:
        if c[0] == "slide":
            pres.setSlide(int(c[1]))
        elif c[0] == "play":
            pres.setSound(c[1])
        elif c[0] == "end":
            ret = False
    return ret
    
def cleanup():
    cleanupDir("assets")
    os.remove("pres.txt")

def main():
    pygame.init()
    setup()
    name = raw_input('Slide file? ')
    cmds = extractSlides(name)
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption(name)
    # pygame.mouse.set_visible(0)

    pres = Present(screen)
    pres.setSlide(1)
    pres.draw()

    #Prepare Game Objects
    clock = pygame.time.Clock()
    run = True
    pause = False
    frame = -1

    #Main Loop
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == KEYDOWN and event.key == K_q:
                run = False
        if not pause:
            frame += 1
        c = cmds.get(frame)
        if not c == None:
            print str(frame)
            print c
            run = execute(c, pres)
        pres.draw()
    cleanup()
    print 'Bye'


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
