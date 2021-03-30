# PyCTracker


## Overview

_PyCTracker_ is a terminal based program that can show you how much course you watched. Usually i watch my courses on Udemy but sometimes when i am out of town where i don't have good net, i download course for offline use.


This is one of my first programs that i wrote in Python and to be true with you i fell in love with it. This repo don't have some pratical usage except  that you can see one of the methods how to read metadata of videos.


## Setup

1. Download [MediaInfo](https://mediaarea.net/en/MediaInfo) and install it. I installed it in _PROGRAMFILES_ if you install it somewhere else you need to change it in code in _VideoLength.py_ file.
```python
# (LINE 20) mediainfo folder location ( place where you installed mediainfo )
os.chdir(os.environ["PROGRAMFILES"] + "\\mediainfo")

```
2. Download [libmediainfo](https://mediaarea.net/download/source/libmediainfo/19.09/libmediainfo_19.09_AllInclusive.7z) and extract it somewhere
3. Find file __MediaInfoDLL3.py__ in _libmediainfo_0.7.62_AllInclusive.7z\MediaInfoLib\Source\MediaInfoDLL\MediaInfoDLL3.py_
4. Put this file in same folder where you want to place __VideoLength.py__ file

#### Changes in code that you need to make

To make this work you need to change few things.
* Path to videoplayer you want to use i am using KMPlayer
    * ```python
        #(Line 23)this is video player you want to use change it to your location
        videoPlayer = "C://Program Files//KMPlayer 64X//KMPlayer64.exe"
        ```
* Path to file where we are storing data.
    * ```python
        #(LINE 473)location where we save data, replace "path" with your folder location
        with open('"path"\\data.txt','w') as outfile: 
        ```



## Usage

Open your favorite terminal program and navigate to place where you put __MediaInfoDLL3.py__ and __VideoLength.py__ files.
```bash
    python VideoLength.py "path" 
```
for example 
```bash
     python VideoLength.py "D:\Udemy\Beginner Python and Coding Intro - Scripting a Virtual Car" 
```
 If you execute script without arguments you get total time for each course section

![Markdown Logo](https://user-images.githubusercontent.com/44332939/73797928-9acb0000-47b1-11ea-9b9a-af2b0a56fac1.PNG)





## Arguments 

You can pass some arguments 

| Argument | Usage                                      | Example                             |
|----------|--------------------------------------------|-------------------------------------|
| -s       | length of specified section                |  VideoLength.py "path" -s 1         |
| -v       | open folder location of course             |  VideoLength.py "path" -s 1 -v      |
| -p       | play all section videos with video player  |  VideoLength.py "path" -s 1 -v -p   |
| -t       | get course progress                        | VideoLength.py "path" -s 1 -v -p -t |

> Argument -t must be used with -s argument


![Markdown Logo](https://user-images.githubusercontent.com/44332939/73798102-293f8180-47b2-11ea-8b6e-2e2bb2170be3.PNG)




[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

