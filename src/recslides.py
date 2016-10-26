
#Import Modules
import os, pygame
import os.path
import time
from zipfile import ZipFile


from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from prutil import *
from prsound import *
from prpresent import *


def setup():
    setupDir("assets")

def extractSlides(name):
    return extractDir(name + ".zip", 'assets')

def cleanup(name):
    zipDir("assets", "assets.zip")
    cleanupDir("assets")
    fout = ZipFile(name + "_rec.zip", 'w')
    fout.write("assets.zip")
    fout.write("pres.txt")
    fout.close()
    os.remove("assets.zip")
    os.remove("pres.txt")

def main():
    pygame.init()
    setup()
    name = raw_input('Slide file? ')
    snum = extractSlides(name)
    print snum

    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption(name)
    # pygame.mouse.set_visible(0)

    pres = Present(screen)
    pres.setSlide(1)
    pres.draw()
    
    fout = open("pres.txt", 'w')
    fout.write('0:\n')
    fout.write('\tslide 1\n')
    fstr = ""

    #Prepare Game Objects
    clock = pygame.time.Clock()
    curslide = 0
    oldslide = 0
    pauseslide = None
    run = True
    pause = True
    frame = 0
    CHUNK = 4096
    wavout = None
    buf = []
    cmds = []
    p, stream = initSoundStream()
    oldtime = 0
    curtime = 0
    tottime = 0
    eframe = 0
    #Main Loop
    while run:
        clock.tick(60)
        oldtime = curtime
        curtime = time.time()
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == KEYDOWN and event.key == K_q:
                run = False
            elif event.type == KEYDOWN and event.key == K_k:
                pause = not pause
                if pause:
                    print "Pausing on frame " + str(frame) + '/' + str(tottime)
                    writeSound(p, wavout, buf)
                    pauseslide = curslide
                    buf = []
                else:
                    eframe = int(60 * tottime)
                    tottime -= curtime - oldtime
                    print "Unpausing on frame " + str(frame + 1) + '/' + str(tottime + curtime - oldtime)
                    wavout = str(eframe) + ".wav"
                    cmds.append("play " + wavout)
                    if not pauseslide == curslide:
                        cmds.append("slide " + str(curslide + 1))
            elif event.type == KEYDOWN and event.key == K_j:
                curslide = ((curslide - 1) % snum + snum) % snum
            elif event.type == KEYDOWN and event.key == K_l:
                curslide = ((curslide + 1) % snum + snum) % snum
            elif event.type == MOUSEBUTTONDOWN:
                curslide = ((curslide + 1) % snum + snum) % snum
        data = stream.read(CHUNK)
        if not pause:
            frame += 1
            tottime += curtime - oldtime
            eframe = int(60 * tottime)
            buf.append(data)
        if not oldslide == curslide:
            pres.setSlide(curslide + 1)
            cmds.append("slide " + str(curslide + 1))
            oldslide = curslide
            print 'Showing side ' + str(curslide + 1) + '/' + str(snum) + ' (' + str(curslide) + ')'
        if len(cmds) > 0:
            if not pause:
                fstr = fstr + str(eframe) + ':\n'
                for c in cmds:
                    fstr = fstr + '\t' + c + '\n'
            cmds = []
        pres.draw()
    if not pause:
        writeSound(p, wavout, buf)
    fout.write(fstr)
    fout.write(str(eframe) + ':\n')
    fout.write('\tend\n')
    fout.close()
    cleanSoundStream(p, stream)
    cleanup(name)
    print 'Bye'


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
