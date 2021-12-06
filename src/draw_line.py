import cv2
import uuid
import copy
import json
import argparse
import numpy as np 


pt1_x , pt1_y = None , None
list_point = []

def scheme_region(pair_point):
    return {
        "regionID": str(uuid.uuid4()),
        "type": "line",
        "name": "",
        "points":pair_point
    }

def line_drawing(event, x, y, flags, param):
    global pt1_x, pt1_y, img, cache, tmp
    cache = []
    if event==cv2.EVENT_LBUTTONDOWN:
        pt1_x,pt1_y=x,y
        list_point.append((pt1_x, pt1_y))
        cache = copy.deepcopy(img)
        tmp.append(cache)

    elif event==cv2.EVENT_LBUTTONUP:
        list_point.append((x,y))
        img = cv2.line(img,(pt1_x,pt1_y),(x,y),color=(255,255,255),thickness=3)
        print(list_point)   

    elif event==cv2.EVENT_MBUTTONDOWN:
        del list_point[-2:]
        img = tmp[-1]
        del tmp[-1]
        cv2.imshow('test draw', img)
        print(list_point)

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
while(True):
    cv2.imshow('test draw',img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()

output = 'line_poly/' + args.input_uri.split('.')[0] + '_line.json'

scheme = []
for i in range(0,len(list_point), 2):
    scheme.append(scheme_region(str(str(list_point[i]) + ', ' + str(list_point[i+1]))))

with open(output,'w') as f:
    json.dump(scheme, f, indent=4, ensure_ascii=False)    
print('Completed ' + output + ' !')
