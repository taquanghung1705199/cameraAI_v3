#!/bin/bash

BASEDIR=$(dirname "$0")
DIR=$BASEDIR/../fastmot/models

set -e

pip3 install gdown

gdown https://drive.google.com/uc?id=1q2Pa72kOowqKiikFpkqJbtViaKSyz1Rg -O $DIR/osnet_x0_25_msmt17.onnx
gdown https://drive.google.com/uc?id=1C67E3jYieYNiUgdL1TkQsDuTXvr4wF4g -O $DIR/osnet_x0_25_msmt17.trt
gdown https://drive.google.com/uc?id=1wDMNTwLJS_Mnf5Sf_mT-PCeuRHi_TAzO -O $DIR/yolov4-608.onnx
gdown https://drive.google.com/uc?id=1jL7AJ7YLYzBbbAiBpS_DolcHc3vT4fCr -O $DIR/yolov4-608.trt


