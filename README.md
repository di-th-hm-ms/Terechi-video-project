# Terechi-video-project

## Environment
- Google colaboratory
## Procedure
### install youtube-dl
- pip install youtube_dl -U
- !youtube-dl https://youtu.be/7h-8Dd4CRTY
### install whisper
- !pip install git+https://github.com/openai/whisper.git
- execute this code below

```
import whisper
model = whisper.load_model("large");
path ="/content/friends1.mkv"
result = model.transcribe(path, verbose=True)
print(result)
```
