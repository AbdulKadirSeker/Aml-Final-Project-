import gzip
import shutil
import os
from itertools import compress


def CompressToGZ(path,name, remove_original = False, compresslevel = 9):
    completepath = os.path.join(path,name)
    newpath = completepath+'.gz'
    with open(completepath,'rb') as f_in:
        with gzip.open(newpath,'wb', compresslevel= compresslevel) as f_out:
            shutil.copyfileobj(f_in, f_out)
    if remove_original:
        os.remove(completepath)

def CompressAllToGZ(path):
    for file in os.listdir(path):
        CompressToGZ(path,file)


# CompressAllToGZ('../../../Data(Final Project)')