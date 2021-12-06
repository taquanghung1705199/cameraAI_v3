import cv2
import copy
import argparse
import numpy as np 

pt1_x , pt1_y = None , None
list_point = []

def line_drawing(event, x, y, flags, param):
    global pt1_x, pt1_y, img, cache, tmp
    cache = []
    if event==cv2.EVENT_LBUTTONDOWN:
        pt1_x,pt1_y=x,y
        list_point.append([pt1_x, pt1_y])
        cache = copy.deepcopy(img)
        tmp.append(cache)

    elif event==cv2.EVENT_LBUTTONUP:
        list_point.append([x,y])
        img = cv2.rectangle(img,(pt1_x,pt1_y),(x,y),color=(255,255,255),thickness=3)
        print(list_point)   

    elif event==cv2.EVENT_RBUTTONDOWN:
        try:
            del list_point[-2:]
            img = tmp[-1]
            del tmp[-1]
            cv2.imshow('test draw', img)
            print(list_point)
        except IndexError:
            pass
        

global img
global cache  
global tmp
tmp = []  


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i', '--input_uri', metavar="URI", required=True, help=
                    'URL of image background')
# parser.add_argument('-o', '--output_uri', metavar="URI", help='file txt contains coor')
args = parser.parse_args()
img = cv2.imread(args.input_uri)
cv2.namedWindow('test draw')
cv2.setMouseCallback('test draw',line_drawing)
while(1):
    cv2.imshow('test draw',img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()

output = 'line_rec/' + args.input_uri.split('.')[0] + '_rec.txt'
for i in range(0, len(list_point), 2):
    x1 = list_point[i][0]
    y1 = list_point[i][1]
    x2 = list_point[i+1][0]
    y2 = list_point[i+1][1]
    list_point[i][0] = min(x1,x2)
    list_point[i][1] = min(y1,y2)
    list_point[i+1][0] = max(x1,x2)
    list_point[i+1][1] = max(y1,y2)

l = []
for i in list_point:
    l.append(tuple(i))


with open(output,'w') as txt:
    for i in l:
        txt.write(str(i) + "\n")
    print('Completed' + output + ' !')
