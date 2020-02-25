#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image
import glob


# In[ ]:


folder_path = '../result/graphs_normalized/'


# In[ ]:


paths =  glob.glob(folder_path+"*.png")
paths.sort()


# In[ ]:


imagelist=[]


# In[ ]:


for path in paths:
    image = Image.open(path)
    imagelist.append(image.convert('RGB'))


# In[ ]:


imagelist[0].save(r'normalized.pdf',save_all=True, append_images=imagelist[1:])

