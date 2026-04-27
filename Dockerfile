FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

RUN apt update && apt install -y python3 python3-pip ffmpeg

RUN pip3 install faster-whisper

WORKDIR /data

COPY transcribe.py /app/transcribe.py

ENTRYPOINT ["python3", "/app/transcribe.py"]