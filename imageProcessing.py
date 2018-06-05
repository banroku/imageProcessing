# -*- coding: utf-8 -*-
"""
Folder tree
    /original
    /underProcessing

1. Put your images in original 
2. Run initializeFolder() to cp original/* to underProcessing/
3. Run processing functions, generally
    1. resize()
    2. addText()
    3. concatenateImage()
*if checkOnly=True, only display first file processed, and not save.

@author: fuji sakai
"""

import os
import shutil
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

folder_original = 'original'
folder_processing = 'underProcessing'

def initializeFolder():
    shutil.rmtree(folder_processing)
    shutil.copytree(folder_original, folder_processing)

def resizeImage(size=(256, 192), checkOnly=False):
    files = os.listdir(folder_processing)
    for i in range(0, len(files)):
        file = files[i]
        img = Image.open(os.path.join(folder_processing, file))
        img = img.resize(size)
        if checkOnly == True: 
            img.show()
            break
        img.save(os.path.join(folder_processing, file))

def addTitle(fontsize=15, checkOnly=False):
    myfont = ImageFont.truetype("arial.ttf", fontsize)
    pos = (5, 5)
    files = os.listdir(folder_processing)
    for i in range(0, len(files)):
        file = files[i]
        title, ext = os.path.splitext(file)
        img = Image.open(os.path.join(folder_processing, file))
        draw = ImageDraw.Draw(img)
        draw.text(pos, title, (255, 255, 255), font = myfont)
        if checkOnly == True: 
            img.show()
            break
        img.save(os.path.join(folder_processing, file))

def concatenateImage(batch_size=1, batch_in_row=False,
    space=10, checkOnly=False, output_name ="concatenated.jpg"):

    files = os.listdir(folder_processing)
    nb_samples = len(files) // batch_size
    img = Image.open(os.path.join(folder_processing, files[0]))
    width, height = img.size
    width = width + space
    height = height + space
    
    if batch_in_row:
        output_size = (width * batch_size - space, height * nb_samples - space)
    else:
        output_size = (width * nb_samples - space, height * batch_size - space)

    output = Image.new(mode='RGB', color=(255, 255, 255), size=output_size)
    
    for i in range(0, nb_samples):
        for j in range(0, batch_size):
            
            file = files[batch_size * i + j]
            img = Image.open(os.path.join(folder_processing, file))
            if batch_in_row:
                output.paste(img, (width * j, height * i))
            else:
                output.paste(img, (width * i, height * j))

    if checkOnly == True:
        output.show()
    else:
        output.save(os.path.join(os.path.curdir, output_name))
