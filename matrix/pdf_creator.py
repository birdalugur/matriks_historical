#!/usr/bin/env python
# coding: utf-8


from PIL import Image
import glob

folder_path = 'results/graphs/'
folder_path2 = 'results/graphs_normalized/'

paths = glob.glob(folder_path + "*.png")
paths.sort()

imagelist = []

for path in paths:
    image = Image.open(path)
    imagelist.append(image.convert('RGB'))

imagelist[0].save(r'all_graphics.pdf', save_all=True, append_images=imagelist[1:])
