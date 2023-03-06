import cv2
import os
import time
import math
import numpy
from PIL import Image

ROI_top = 250
ROI_bottom = 850
ROI_right = 1150
ROI_left = 1750

black_filter=0.2 #may be adjusted, the more closer to 0, the blacker it is

def check_L(path):
    #L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    image = Image.open(path)

    luminance = numpy.empty((27,27), dtype=bool)
    
    rgb_image = image.convert('RGB')
    for y in range(27):
        for x in range(27):
            r,g,b = rgb_image.getpixel((x, y))
            if ((0.2126 * r + 0.7152 * g + 0.0722 * b)/255<black_filter):
                luminance[x][y] = True

            else:
                luminance[x][y] = False
    
    return(luminance)

def hollow_shape(shape):
    # Create a new array to hold the hollowed shape
    hollowed_shape = [[False] * 27 for _ in range(27)]

    # Loop through each row and column of the shape array
    for i in range(27):
        for j in range(27):
            # If the current element is True
            if shape[i][j]:
                # Check if any of the adjacent elements are False
                if i > 0 and not shape[i-1][j]:
                    hollowed_shape[i][j] = True
                elif i < 26 and not shape[i+1][j]:
                    hollowed_shape[i][j] = True
                elif j > 0 and not shape[i][j-1]:
                    hollowed_shape[i][j] = True
                elif j < 26 and not shape[i][j+1]:
                    hollowed_shape[i][j] = True

    return hollowed_shape


def linearize(map):
    sum_x=0
    sum_y=0
    sum_xy=0 
    sum_x2=0
    n = len(map)
    if n > 1:
        for i in range (n-1):
            sum_x = sum_x + map[i][0]
            sum_y = sum_y + map[i][1]
            sum_xy = sum_xy + map[i][0] * map[i][1]
            sum_x2 = sum_x2 + map[i][0] * map[i][0]
        return (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x2)
    else:
        return "error"

def correlate(map):
    sum_x=0
    sum_y=0
    sum_xy=0
    sum_x2=0
    sum_y2 = 0
    n = len(map)
    if n > 1:
        for i in range (n-1):
            sum_x = sum_x + map[i][0]
            sum_y = sum_y + map[i][1]
            sum_xy = sum_xy + map[i][0] * map[i][1]
            sum_x2 = sum_x2 + map[i][0] * map[i][0]
            sum_y2 = sum_y2 + map[i][1] * map[i][1]
        return (n * sum_xy - sum_x * sum_y) / math.sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y))
    else:
        return "error"

def exec_(path):
    os.system("clear")
    map = []
    image_arr = hollow_shape(check_L(path))
    print(image_arr)
    for y in range(27):
        for x in range(27):
            if image_arr[x][y]==True:
                map.append([x,y])    
    map = numpy.array(map)
    print("m = ", linearize(map))
    print("r = ", correlate(map))

cam = cv2.VideoCapture(0)

while True:
    result, image = cam.read()
    image = cv2.flip(image, 1)
    roi = image[ROI_top:ROI_bottom, ROI_right:ROI_left]
    cv2.rectangle(image, (ROI_left,ROI_top), (ROI_right,ROI_bottom), (0,0,255), 3)
    cv2.imshow("test",image)
    key = cv2.waitKey(1)
    if key == 27: #esc
        break
    elif key == 13: #enter
        cv2.imwrite("test.png",roi)
        time.sleep(1) #buffer, time may be manipulated for performance
        foo=cv2.imread("test.png") 
        foo=cv2.resize(foo, (27,27))
        cv2.imwrite("test.png",foo)
        exec_("test.png")

cam.release()
cv2.destroyAllWindows()