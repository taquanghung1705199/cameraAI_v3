ARG TRT_IMAGE_VERSION=21.05
FROM nvcr.io/nvidia/tensorrt:${TRT_IMAGE_VERSION}-py3

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Ho_Chi_Minh

RUN mkdir /FastMOT
COPY requirements.txt /FastMOT

RUN pip install -U pip && \
    pip install --no-cache-dir cython && \
    pip install --no-cache-dir -r /FastMOT/requirements.txt && \
    apt update && \
    apt install ffmpeg -y

WORKDIR /FastMOT
