#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 07:18:55 2019

@author: quintonnixon
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 18:42:43 2019

@author: quintonnixon
"""

import cv2
import pandas as pd
import numpy as np
import os

# replace with your local directory where you have the core samples stored
mydir = '/Users/quintonnixon/Documents/@Grad School/@SMU/@Term_5_Courses/Capstone_B/images'

def createFileList(myDir, format='.jpg'):
    fileList = []
    print('\nCurrent Working Directory:\n', myDir, end='\n')
    
    for root, dirs, files in os.walk(myDir, topdown=False):
        for file in files:
            if file.endswith(format):
                fullName = os.path.join(root, file)
                fileList.append(fullName)
        print('\nList of Core Images:\n', fileList, end='\n')
    return fileList

fileList = createFileList(mydir)

fileList.sort()
fileList

# gets all images in the directory
test_images = [cv2.imread(file) for file in fileList]

# check to make sure the files are what you think they are
print('image 1 Shape:', test_images[0].shape)
print('image 1 Shape:', test_images[1].shape)

# make working copy of one core image
sample_image = test_images[0].copy()

# resize to 25%
resized_image = cv2.resize(sample_image,(340,7500))
print(resized_image.shape)

# extract center portion
extracted_center_portion = resized_image[:, 120:220]
print(extracted_center_portion.shape)

# convert to RGB
center_portion_RGB = cv2.cvtColor(extracted_center_portion, cv2.COLOR_BGR2RGB)

# convert to LAB
center_portion_LAB = cv2.cvtColor(extracted_center_portion, cv2.COLOR_BGR2LAB)

# convert to grayscale
center_portion_GRAY = cv2.cvtColor(extracted_center_portion, cv2.COLOR_BGR2GRAY)

# Get the center_portion_RGB data from image into a dataset
r1 = []
g1 = []
b1 = []

for line in center_portion_RGB[:, :]:

    for pixel in line:

        temp_r, temp_g, temp_b = pixel

        r1.append(temp_r)

        g1.append(temp_g)

        b1.append(temp_b)
        
center_portion_RGB_data = pd.DataFrame({'Red': r1, 'Green': g1, 'Blue': b1})
center_portion_RGB_data.head()

# Get the center_portion_GRAY data from image into a dataset
w1 = []

for line in center_portion_GRAY[:, :]:
    
    for pixel in line:

        temp_w = pixel

        w1.append(temp_w)
  
center_portion_GRAY_data = pd.DataFrame({'Gray': w1})
center_portion_GRAY_data.head()

# Get L* for the center portion
L_star = []
a_star = []
b_star = []

for line in center_portion_LAB[:, :]:

    for pixel in line:

        temp_L_star, temp_a_star, temp_b_star = pixel

        L_star.append(temp_L_star)

        a_star.append(temp_a_star)

        b_star.append(temp_b_star)
        
center_portion_LAB_data = pd.DataFrame({'Lstar': L_star})
center_portion_LAB_data.head()

# merge RGB, grayscale, and L* values
merged_image_data = center_portion_RGB_data.merge(center_portion_GRAY_data, left_index=True, right_index=True)
merged_image_data = merged_image_data[['Red', 'Green', 'Blue', 'Gray']]
merged_image_data = merged_image_data.merge(center_portion_LAB_data, left_index=True, right_index=True)
merged_image_data = merged_image_data[['Red', 'Green', 'Blue', 'Gray', 'Lstar']]

# make working copy of merged_image_data for filtering out dark and light pixels
filtered_image_data = merged_image_data.copy()

# replace darkest 35% with NaN
dark_mask = filtered_image_data.Lstar <= 35
column_names = ['Red', 'Green', 'Blue', 'Gray', 'Lstar']
filtered_image_data.loc[dark_mask, column_names] = np.NAN

# replace lightest 15% with NaN
light_mask = filtered_image_data.Lstar >= 85
filtered_image_data.loc[light_mask, column_names] = np.NAN

# average over every 100 rows which should return a 7500x5 dataframe with avg R, G, B, Gray, and L* for the sample
filtered_image_average_values = filtered_image_data.groupby(np.arange(len(filtered_image_data))//100).mean()
filtered_image_average_values.shape