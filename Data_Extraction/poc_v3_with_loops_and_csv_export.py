import cv2
import numpy as np
import os
import csv

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

# check number of files
len(test_images)

# check to make sure the files are what you think they are and have the right shape
for i in range(len(test_images)):
    print('image ' + str(i) + ' shape:', test_images[0].shape)

# make working copy of one core image
sample_images = test_images.copy()


# resize images to specific size
# enter the desired scale percentage (i.e. percent of original size)
scale_percent = 100
resized_images = [None] * len(sample_images) # create empty list for resized images

for j in range(len(sample_images)):
    width = int(sample_images[j].shape[1] * scale_percent / 100)
    height = int(sample_images[j].shape[0] * scale_percent / 100)
    # resize image and write to new list
    resized_images[j] = cv2.resize(sample_images[j], (width, height))
 
# check resized dimiensions
for l in range(len(resized_images)):
    print('Resized image ' + str(l) + ' shape:', resized_images[0].shape)   
    
# extract center portion of specified width (must be less than total width)
desired_width = 200   
half_width = int(desired_width/2)

# create empty list to hold the extracted center portions
extracted_center_portions = [None] * len(resized_images)

# loop through the resized images, extract the center portion and write that to the list
for m in range(len(resized_images)):
    center = int(resized_images[m].shape[1]/2)
    extracted_center_portions[m] = resized_images[m][:, center - half_width:center + half_width]

# convert center portions to RGB, LAB, and Grayscale
# create empty lists for holding the RGB, Grayscale, and LAB values    
center_portions_RGB = [None] * len(extracted_center_portions) 
center_portions_LAB = [None] * len(extracted_center_portions) 
center_portions_GRAY = [None] * len(extracted_center_portions) 

# loop through each center portion and make the conversions
for n in range(len(extracted_center_portions)):
    center_portions_RGB[n] = cv2.cvtColor(extracted_center_portions[n], cv2.COLOR_BGR2RGB)
    center_portions_LAB[n] = cv2.cvtColor(extracted_center_portions[n], cv2.COLOR_BGR2LAB)
    center_portions_GRAY[n] = cv2.cvtColor(extracted_center_portions[n], cv2.COLOR_BGR2GRAY)

# create an empty list to hold r,g,b,gray, and L* for each image by row and pixel
color_space_values = [None] * len(extracted_center_portions) 

# loop through each center portion, by row and pixel and write the values of interest 
# to a location in the color_space_values list
# each pixel will have a corresponding array of R, G, B, Grayscale, and L* values for later manipulation
for o in range(len(extracted_center_portions)):
    temp_array = np.zeros(shape=(center_portions_RGB[o].shape[0],center_portions_RGB[o].shape[1], 5))
    for p in range(center_portions_RGB[o].shape[0]):
        for q in range(center_portions_RGB[o].shape[1]):
            red_current_pixel = center_portions_RGB[o][p][q][0]
            green_current_pixel = center_portions_RGB[o][p][q][1]
            blue_current_pixel = center_portions_RGB[o][p][q][2]
            gray_current_pixel = center_portions_GRAY[o][p][q]
            L_star_current_pixel = center_portions_LAB[o][p][q][0]
            temp_array[p][q] = [red_current_pixel, 
                              green_current_pixel, 
                              blue_current_pixel, 
                              gray_current_pixel, 
                              L_star_current_pixel]
    color_space_values[o] = temp_array        

# calculate average values for each row
# create empty list to hold the average values for each of the color_space_value arrays
# that correspond to the center sections    
avg_color_space_values = [None] * len(color_space_values)

# loop through each color_space_value array and calculate average values
# for pixels with L* in the middle 50% of the L* range
for r in range(len(color_space_values)):
    # create empty list to hold temporary average values
    temp_array_2 = np.zeros(shape=(color_space_values[r].shape[0], 5))
    for s in range(color_space_values[r].shape[0]):
        # initialize variables for totals and count
        # count is being set to one to avoid a possible divide by zero
        r_tot = 0
        g_tot = 0
        b_tot = 0
        gray_tot = 0
        L_star_tot = 0
        count = 1
        for t in range(color_space_values[r].shape[1]):
            # this if statement sets the L* thresholds for determining whether
            # or not to use a pixel for calculating an average value
            if 89 <= color_space_values[r][s][t][4] <= 217:
                r_tot = r_tot + color_space_values[r][s][t][0]
                g_tot = g_tot + color_space_values[r][s][t][1]
                b_tot = b_tot + color_space_values[r][s][t][2]
                gray_tot = gray_tot + color_space_values[r][s][t][3]
                L_star_tot = L_star_tot + color_space_values[r][s][t][4]
                count += 1
        avg_r = r_tot / count
        avg_g = g_tot / count
        avg_b = b_tot / count
        avg_gray = gray_tot / count
        avg_L = L_star_tot / count
        temp_array_2[s] = [avg_r, avg_g, avg_b, avg_gray, avg_L]   
    avg_color_space_values[r] = temp_array_2
    
# avg_color_space should contain X arrays that correspond to the average
# R, G, B, Grayscale, and L* values for each row of each core sample in the
# original file directory.  These areas can be combined into a single tall
# arrary or handled individually for further modeling/manipulation    
    

# output each color_space_value array to a separate csv for external analysis
for u in range(len(avg_color_space_values)): 
    filename = 'avg_color_space_values_for_image%d.csv'%(u,)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(avg_color_space_values[u])

