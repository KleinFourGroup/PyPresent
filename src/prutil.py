
import os
import os.path
from zipfile import ZipFile


def setupDir(loc):
    if not os.path.isdir(loc):
        os.mkdir(loc)
    else:
        for top, dirs, names in os.walk(loc, topdown=False):
            for name in names:
                rm = os.path.join(loc, name)
                os.remove(rm)

def extractDir(loc, dest):
    snum = 0
    fin = ZipFile(loc, 'r')
    for slide in fin.namelist():
        snum += 1
        fin.extract(slide, dest)
    fin.close()
    return snum

def zipDir(loc, dest):
    fout = ZipFile(dest, 'w')
    for top, dirs, names in os.walk(loc, topdown=False):
        for name in names:
            zf = os.path.join(loc, name)
            fout.write(zf, name)
    fout.close()

def cleanupDir(loc):
    for top, dirs, names in os.walk(loc, topdown=False):
        for name in names:
            rm = os.path.join(loc, name)
            os.remove(rm)
    os.rmdir(loc)
