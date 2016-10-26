
#Import Modules
import os
import os.path
from zipfile import ZipFile

import wand.image, wand.color

def setup():
    if not os.path.isdir("png"):
        os.mkdir("png")
    else:
        for png, dirs, slides in os.walk("png", topdown=False):
            for slide in slides:
                loc = os.path.join(png, slide)
                os.remove(loc)

def cleanup(name):
    fout = ZipFile(name + ".zip", 'w')
    for png, dirs, slides in os.walk("png", topdown=False):
        for slide in slides:
            loc = os.path.join(png, slide)
            fout.write(loc, slide)
            os.remove(loc)
    os.rmdir("png")
    fout.close()

def fileToSlides(loc, num_slides, start = 1, end = "len"):
    try:
        img_file = wand.image.Image(filename=loc, resolution=300)
    except:
        print "ERROR: BAD FILE"
        return num_slides
    if start == None or end == None:
        print "ERROR: BOUNDS MUST BE INTS"
        return num_slides
    if start == "len":
        start = len(img_file.sequence)
    if end == "len":
        end = len(img_file.sequence)
    if start < 1 or end > len(img_file.sequence) or end < start:
        print "ERROR: OUT OF BOUNDS"
        return num_slides
    print "Reading pages " + str(start) + " to " + str(end) + " of " + loc
    for i in range(start - 1, end):
        page = img_file.sequence[i]
        with wand.image.Image(page) as pi:
            pi.format = 'png'
            pi.background_color = wand.color.Color('white')
            pi.alpha_channel = False
            fout = os.path.join('png', str(num_slides + 1) + ".png")
            pi.save(filename=fout)
        num_slides += 1
    return num_slides

def toPage(i):
    if i == "len":
        return i
    try:
        i = int(i)
        return i
    except ValueError:
        return None

def main():
    setup()
    name = raw_input('Name? ')
    snum = 0
    run = True
    while run:
        prompt = raw_input('> ')
        argv = prompt.split()
        if len(argv) == 0:
            pass
        else:
            cmd = argv[0]
            if cmd == "load":
                if len(argv) == 2:
                    loc = argv[1]
                    snum = fileToSlides(loc, snum)
                elif len(argv) == 3:
                    loc = argv[1]
                    s = toPage(argv[2])
                    e = s
                    snum = fileToSlides(loc, snum, s, e)
                elif len(argv) == 4:
                    loc = argv[1]
                    s = toPage(argv[2])
                    e = toPage(argv[3])
                    snum = fileToSlides(loc, snum, s, e)
                else:
                    print "ERROR: BAD COMMAND"
            elif cmd == "num":
                if len(argv) == 1:
                    print name + " currently has " + str(snum) + " slides"
                else:
                    print "ERROR: BAD COMMAND"
            elif cmd == "quit" or cmd == "q":
                if len(argv) == 1:
                    run = False
                else:
                    print "ERROR: BAD COMMAND"
    cleanup(name)
    print 'Bye'



#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
