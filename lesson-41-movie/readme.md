# MoviePy
- https://zulko.github.io/moviepy/
- https://github.com/Zulko/moviepy

# Apps
## GPT MultiModal by Parallel75
- https://github.com/parallel75/GPT_Multimodal/tree/main

# Setup
## install pytube (optional)
download youtube videos (see https://github.com/wgong/py4kids/tree/master/lesson-99-misc/pytube)

## install pyGame (optional) 

## install imagemagick (required)

https://www.imagemagick.org/script/download.php

## clone source
```
conda create -n movie
conda activate movie

cd ~\projects\wgong\FUN
git clone git@github.com:Zulko/moviepy.git
python setup.py install
pip show moviepy

# Name: moviepy
# Version: 2.0.0.dev0
# Summary: Video editing with Python
# Home-page: https://zulko.github.io/moviepy/
# Author: Zulko 2017
```
not working because v2.0 is under development

```
pip install moviepy
# Version: 1.0.3
```


## local
dir = ~\projects\wgong\FUN\moviepy

```
cd $dir
pip install moviepy
pip install moviepy[optional]
pip install moviepy[doc] 
```


