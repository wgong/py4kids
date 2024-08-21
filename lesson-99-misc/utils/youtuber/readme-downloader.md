# YouTube Downloader 

- https://stackshare.io/pypi-pytube/alternatives#:~:text=ClipGrab%3A%20ClipGrab%20is%20a%20free,platform%20support%20and%20simple%20interface.



# yt-dlp
- https://www.reddit.com/r/Python/comments/18wzsg8/good_pytube_alternative/

it offers 2 features I like

extract audio only format,
my main usage is to listen music offline, so this feature would save storage too.
specify video_id instead of URL.
This CLI tool has tons of options, need to read documentation to get used to
To get started quickly, do the following (3ug835LFixU is the YT video_id as an example)

```
pip install yt-dlp


# TD Lee on neutrino
# https://www.youtube.com/watch?v=0pn5PCAFVv8
yt-dlp 0pn5PCAFVv8  

# TD Lee - Challenge of Physics at Great Hall of People (I)
yt-dlp AqzaBE8stbA 
# T.D. Lee's public lecture: challenges in physics (II) (in Chinese)
# https://www.youtube.com/watch?v=WqX9k5hrCyY
yt-dlp WqX9k5hrCyY
# T.D. Lee's public lecture: challenges in physics (III) (in Chinese)
# https://www.youtube.com/watch?v=vX6FF6ljSdE
yt-dlp vX6FF6ljSdE

yt-dlp -x --audio-format mp3 3ug835LFixU   # Beethoven Symphony 5
yt-dlp -x --audio-format mp3 4IqnVCc-Yqo   # Beethoven Symphony 9
yt-dlp -x --audio-format mp3 i1JrOGXGQSI   # Butterfly Lovers violin concerto
```

https://github.com/pytube/pytube/issues/1954



# pytube 

# Install
```
conda create -n movie python=3.11
conda activate movie
pip install pytube PyYaml
#Version: 15.0.0
#Location: C:\Users\p2p2l\anaconda3\envs\movie\Lib\site-packages
```

# Docs
https://pytube.io/en/latest/user/quickstart.html

# CLI

## run `pytube` exe on command line:
```
pytube https://www.youtube.com/watch?v=Xh5rFHYZS8Y
```

## enter video URL in `youtube-list.yaml` file,
```
cd C:\Users\p2p2l\Videos\My_Downloader
python download_youtube.py
```


# Bugs:

- [2024-08-11] pytube.exceptions.RegexMatchError: map_functions: could not find match for multiple

## Error
```
  File "C:\Users\p2p2l\anaconda3\lib\site-packages\pytube\cipher.py", line 250, in get_transform_map
    fn = map_functions(function)
  File "C:\Users\p2p2l\anaconda3\lib\site-packages\pytube\cipher.py", line 704, in map_functions
    raise RegexMatchError(caller="map_functions", pattern="multiple")
pytube.exceptions.RegexMatchError: map_functions: could not find match for multiple
```

```
    function_patterns = [
        # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
        # https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
        # var Bpa = [iha];
        # ...
        # a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
        # Bpa.length || iha("")) }};
        # In the above case, `iha` is the relevant function name
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
    ]
```
## Fix?


Change the function_patterns array in cipher.py at line 264 to include this one and it seems to work:
```
	function_patterns = [
		# https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
		# https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
		# var Bpa = [iha];
		# ...
		# a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
		# Bpa.length || iha("")) }};
		# In the above case, `iha` is the relevant function name
		r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
		r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
		r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
	]

```


How to get real-time song lyrics and sing along with Apple Music and Shazam
https://www.idownloadblog.com/2019/04/25/real-time-shazam-song-lyrics/

English songs with lyrics:

https://www.lyrics.com/

https://www.lyrics.com/artist/The-Phantom-Of-The-Opera-Original-London-Cast/2137964643


https://www.lyrics.com/lyric/36111174/Madonna/Like+a+Virgin
https://www.lyrics.com/lyric/2734751/Madonna/Like+a+Prayer

https://www.lyrics.com/lyric/36111222/Madonna/Holiday

https://www.lyrics.com/lyric/34917877/Madonna/Open+Your+Heart

https://www.lyrics.com/lyric/35736998/Madonna/Express+Yourself

https://www.lyrics.com/lyric/35736982/Madonna/Crazy+for+You

https://www.lyrics.com/lyric/35459779/Madonna/Material+Girl


https://www.allthelyrics.com/lyrics/beauty_and_the_beast_soundtrack
https://www.allthelyrics.com/lyrics/beauty_and_the_beast_soundtrack/beauty_and_the_beast-lyrics-74986.html


https://www.allthelyrics.com/lyrics/celine_dion
https://www.allthelyrics.com/lyrics/celine_dion/a_new_day_has_come-lyrics-29282.html


Chinese songs with lyrics:


https://www.echinesesong.com/xiang-lian-%E4%B9%A1%E6%81%8B-lyrics-%E6%AD%8C%E8%A9%9E-with-pinyin-by-li-gu-yi-%E6%9D%8E%E8%B0%B7%E4%B8%80/

https://www.echinesesong.com/wang-ning-mei-%e6%9e%89%e5%87%9d%e7%9c%89-frown-lyrics-%e6%ad%8c%e8%a9%9e-with-pinyin-by-chen-li-%e9%99%88%e5%8a%9b/

chén zhōng jīng fēi niǎo 
晨   钟    惊   飞  鸟   
The morning clock flutters the birds
lín jiān xiǎo xī shuǐ chán chán 
林  间   小   溪 水   潺   潺   
The little brook among the trees was a stream


design a simple app
to display song (video) + moving lyrics text 

<marquee direction="up" behavior="scroll" scrollamount=1>
你 的 声    音    你 的 歌 声  
<br><br>
永   远   印  在  我 的 心  中    
<br><br>
昨  天   虽  已 消   失  
<br><br>
分  别  难  相    逢   
<br><br>
怎  能   忘   记 你 的 一 片   深   情   
<br><br>
昨  天   虽  已 消   失  
<br><br>
分  别  难  相    逢   
</marquee>

marquee supported in Brave/Chrome/Firefox browsers

