## Download MP3 from YouTube

- pip install pytubefix / pytube

```
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
url = "your_youtube_url"
yt = YouTube(url, on_progress_callback = on_progress)
ys = yt.streams.filter(only_audio=True).first()
# Following command will download a file_name.mp4
ys.download()

# To download as MP4 first and then remane MP4 to MP3
mp3 = ys.download()
>>> █████████████████████████████████████████████████████████████████████████████████████████| 100.0%
base, ext = os.path.splitext(mp3)
new_file = base + '.mp3'
os.rename(mp3, new_file)
```

## Download MP4 from YouTube

- pip install pytubefix / pytube

```
from pytubefix import YouTube
from pytubefix.cli import on_progress
url = "your_youtube_url"
yt = YouTube(url, on_progress_callback = on_progress)
ys = yt.streams.filter(adaptive=True).order_by("resolution").last()
ys.download()

```
