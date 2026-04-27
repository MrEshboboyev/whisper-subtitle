How to add subtitle (with .srt files) in "folder_path":

Build image:
```
docker build -t whisper-srt .
```

Run image:
```
docker run --rm --gpus all -v ${PWD}:/data whisper-srt /data/<your-folder>
```
