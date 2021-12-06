import cv2
import uuid
import json
import argparse
import numpy as np

tpPointsChoose = []
polygon = []
drawing = False
tempFlag = False

def scheme_region(zone):
    return {
        "regionID": str(uuid.uuid4()),
        "type": "polygon",
        "name": "",
        "points":zone
    }

def draw_ROI(event, x, y, flags, param):
    global point1, tpPointsChoose,pts,drawing, tempFlag, polygon
    if event == cv2.EVENT_LBUTTONDOWN:
        tempFlag = True
        drawing = False
        point1 = (x, y)
        tpPointsChoose.append((x, y))  # Used to draw points
    if event == cv2.EVENT_RBUTTONDOWN:
        tempFlag = True
        drawing = True
        pts = np.array([tpPointsChoose], np.int32)
        pts1 = tpPointsChoose[0:len(tpPointsChoose)]
        # print(pts1)
        polygon.append(pts)
        tpPointsChoose = []
        
    if event == cv2.EVENT_MBUTTONDOWN:
        tempFlag = False
        drawing = True
        tpPointsChoose = []
        try:
            polygon.pop(-1)
        except IndexError:
            pass
cv2.namedWindow('polygon')
cv2.setMouseCallback('polygon',draw_ROI)


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i', '--input_uri', metavar="URI", required=True, help=
                    'URL of image background')
args = parser.parse_args()

while (True):
    img = cv2.imread(args.input_uri)
    if (tempFlag == True and drawing == False) :  # Mouse click
        cv2.circle(img, point1, 5, (0, 255, 0), 2)
        for i in range(len(tpPointsChoose) - 1):
            cv2.line(img, tpPointsChoose[i], tpPointsChoose[i + 1], (255, 0, 0), 2)
    if (tempFlag == True and drawing == True):  #Mouse right click
        # cv2.polylines(img, [pts], True, (0, 0, 255), thickness=1)
        for i in polygon:
            cv2.polylines(img, [i], True, (0, 0, 255), thickness=1)
            
    if (tempFlag == False and drawing == True):  # Middle mouse button
        for i in range(len(tpPointsChoose) - 1):
            cv2.line(img, tpPointsChoose[i], tpPointsChoose[i + 1], (0, 0, 255), 2)
    cv2.imshow('polygon', img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):  # Press q to exit
    #     break
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()

output = 'line_poly/' + args.input_uri.split('.')[0] + '_poly.json'

scheme = []
for i in polygon:
    i = i.tolist()
    for j in i:
        scheme.append(scheme_region(str(j)))

with open(output,'w') as f:
    json.dump(scheme, f, indent=4, ensure_ascii=False)  
print('Completed ' + output + ' !')
