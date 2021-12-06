#!/bin/bash

BASEDIR=$(dirname "$0")
DIR=$BASEDIR/../fastmot/models

set -e

pip3 install gdown

gdown https://drive.google.com/uc?id=1doeODEFrzFJs2s8U1OcVSe3SBnF2CJhR -O $DIR/osnet_x0_25_msmt17.onnx
gdown https://drive.google.com/uc?id=1dEJH-yU3NbKEYQ-0uGpltTl5nYgvTW5C -O $DIR/osnet_x0_25_msmt17.trt
gdown https://drive.google.com/uc?id=1wzAcD-C7jVzVMuYW3D5C7PB4vOY-0Zhf -O $DIR/yolov4-608.onnx
gdown https://drive.google.com/uc?id=1a6L2n8cx3BFm_AhwNes-MJxwIbJ-R_Nj -O $DIR/yolov4-608.trt


