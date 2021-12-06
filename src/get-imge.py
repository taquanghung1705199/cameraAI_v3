import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i', '--input_uri', metavar="URI", required=True, help=
                    'URI to input stream\n'
                    '1) image sequence (e.g. img_%%06d.jpg)\n'
                    '2) video file (e.g. video.mp4)\n'
                    '3) MIPI CSI camera (e.g. csi://0)\n'
                    '4) USB/V4L2 camera (e.g. /dev/video0)\n'
                    '5) RTSP stream (rtsp://<user>:<password>@<ip>:<port>/<path>)\n'
                    '6) HTTP stream (http://<user>:<password>@<ip>:<port>/<path>)\n')
parser.add_argument('-o', '--output_uri', metavar="URI", help='export image \n Ex: S1.jpg')
args = parser.parse_args()

cap = cv2.VideoCapture(args.input_uri)
output = args.output_uri
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, (960, 480), interpolation = cv2.INTER_AREA)
    
    cv2.imwrite(output, frame)
    break
