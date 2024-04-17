import serial
from sklearn.cluster import MeanShift
import cv2
import numpy as np




image = np.zeros((500,500))
image+=127
cv2.circle(image, (250,100), 20, (255,255,0), 2)
#cv2.circle(image, (250,250), 20, (255,255,0), 2)
#cv2.circle(image, (250,400), 20, (255,255,0), 2)
cv2.circle(image, (200,125), 20, (255,255,0), 2)

list = []
#now get x y cords of values
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        if(image[i,j]!=127):
            list.append((i,j))

npArray = np.array(list)

#THIS IS THE PART FOR THE PROJECT BELOW!!!!!!!!!!!

#now use mean shift (define once)
msFunction = MeanShift(bandwidth=60)#change this parameter to include more pixels to mean shift

#determine if there are events
if np.any(npArray):
    # THIS IS WHERE WE PUT THE NP ARRAY OF VALUES FROM SENSOR INTO!!!!!!!!!
    msFunction.fit(npArray)

    # Get the labels for each data point
    labels = msFunction.labels_

    #Get all pixels that correspond to first max
    maxClusterArray = npArray[np.where(labels == 0)]
    maxXValue = np.max(maxClusterArray[:,1])
    minXValue = np.min(maxClusterArray[:,1])
    print(str(maxXValue))
    print(str(minXValue))

    #just get the first one
    point = msFunction.cluster_centers_[0].astype('int')


    cv2.circle(image, (point[1],point[0]), 5, (0,255,0), 5)
    cv2.line(image,(minXValue,0),(minXValue,image.shape[0]),(0, 255, 0),1)
    cv2.line(image, (maxXValue, 0), (maxXValue, image.shape[0]), (0, 255, 0), 1)
    cv2.imwrite("test.png",image)