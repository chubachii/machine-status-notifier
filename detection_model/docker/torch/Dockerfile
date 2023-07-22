# https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel_21-08.html#rel_21-08
# Ubuntu : 20.04
# CUDA   : 11.4.1
# cuDNN  : 8.2.2.26
# Python : 3.8
# PyTorch : 1.10.0 

FROM nvcr.io/nvidia/pytorch:21.08-py3

# 環境変数
# ENV http_proxy 'http://id:pass@proxy:port' など

# コマンド実行
RUN apt-get update && apt-get upgrade -y

# OpenCV エラー回避のため
RUN apt-get install libgl1-mesa-dev -y


# dockerfiles/requirements.txt をコピー
COPY ../requirements.txt .
RUN pip install -r requirements.txt