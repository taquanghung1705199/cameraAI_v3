#!/bin/bash

BASEDIR=$(dirname "$0")
DIR=$BASEDIR/../fastmot/models

set -e

pip3 install gdown

gdown https://drive.google.com/uc?id=1kFNJN5kiX1nKXCDvXa5jv6ac3MfN9gfF -O $DIR/osnet_x0_25_msmt17.onnx
gdown https://drive.google.com/uc?id=18BVifLhRkaBvX74-VZs9pD7WWDgq7n39 -O $DIR/osnet_x0_25_msmt17.trt
#gdown https://drive.google.com/uc?id=1-Cqk2P72P4feYLJGtJFPcCxN5JttzTfX -O $DIR/ssd_inception_v2_coco.pb
#gdown https://drive.google.com/uc?id=1IfSveiXaub-L6PO9mqne5pk2EByzb25z -O $DIR/ssd_mobilenet_v1_coco.pb
#gdown https://drive.google.com/uc?id=1ste0fQevAjF4UqD3JsCtu1rUAwCTmETN -O $DIR/ssd_mobilenet_v2_coco.pb
#gdown https://drive.google.com/uc?id=1-kXZpA6y8pNbDMMD7N--IWIjwqqnAIGZ -O $DIR/yolov4_crowdhuman.onnx
gdown https://drive.google.com/uc?id=1DLw_VKITPyQtA1hWxEafgTPgtNcFiJeT -O $DIR/yolov4-608.cfg
gdown https://drive.google.com/uc?id=1OdTWUUjG1BATypPjZcKH9mLcKKmEBgAk -O $DIR/yolov4-608.onnx
gdown https://drive.google.com/uc?id=1Kq4O_79-rAEbPEZ5gVH7vVju_y9Mirn2 -O $DIR/yolov4-608.trt


