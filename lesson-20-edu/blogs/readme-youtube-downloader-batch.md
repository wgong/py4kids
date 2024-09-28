
## YouTube video downloading tools 

| Tool | Description | Comment |
| youtube-dl | A powerful command-line program to download videos from YouTube and other sites
Very reliable and frequently updated | |
| yt-dlp | A youtube-dl fork with additional features and improvements
Often more up-to-date than youtube-dl | |
| ClipGrab | A free, user-friendly GUI application for downloading videos
| Works on Windows, macOS, and Linux |
| 4K Video Downloader | A user-friendly GUI application with support for various video sites
| Available for Windows, macOS, and Linux
Has both free and paid versions|
| JDownloader | An open-source download management tool
Supports multiple video sites, not just YouTube | |
| VideoProc Converter | A comprehensive video processing tool that includes YouTube download capabilities
| Paid software with a free trial |
| VLC Media Player | While primarily a media player, it can also download YouTube videos
Free and open-source| |

## Batch downloading 

`youtube-dl` and `yt-dlp` are excellent for automation and batch downloading. 
You can create a text file with a list of urls and use it as input for batch processing. 

Lines starting with '#' are treated as comments and ignored.
You can also add comments after the URL on the same line.

For example:
```
yt-dlp -a urls.txt
youtube-dl -a urls.txt

# extracting mp3
yt-dlp -x --audio-format mp3 -a urls.txt
youtube-dl -x --audio-format mp3 -a urls.txt

# extracting mp4
yt-dlp -f 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b' -a urls.txt
youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' -a urls.txt

# Skipping previously downloaded videos
yt-dlp --download-archive downloaded.txt -a urls.txt
youtube-dl --download-archive downloaded.txt -a urls.txt
```