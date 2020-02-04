import os
from colorama import Fore, Back, Style
import argparse
import webbrowser
import subprocess
import time
import json
import re
import random


'''
Mediainfo is used for reading metadata of videos.
https://stackoverflow.com/questions/15041103/get-total-length-of-videos-in-a-particular-directory-in-python/15043503#15043503
https://mediaarea.net/en/MediaInfo
https://mediaarea.net/en/MediaInfo/Download/Source
'''

#mediainfo folder location ( place where you installed mediainfo )
os.chdir(os.environ["PROGRAMFILES"] + "\\mediainfo")
from MediaInfoDLL3 import MediaInfo, Stream

#this is video player you want to use change it to your location
videoPlayer = "C://Program Files//KMPlayer 64X//KMPlayer64.exe"
allowed_ext = [".mp4",".m4v",".mkv",".webm",".mov",".avi",".wmv",".mpg",".flv"]


#argparse is used for reading command line arguments
parser = argparse.ArgumentParser(description='Calculate length of video files in folder')
parser.add_argument('Path', metavar='path', type=str, help='Path to folder you want to use')
group = parser.add_mutually_exclusive_group()
group.add_argument('-o','--one',help='Use this argument if you want to calculate only one folder (default is all folders)', action='store_true')
group.add_argument('-s','--section',help='Use this argument if you want to get specific section can\'t be used with -o ', type=int,default=-1)
parser.add_argument('-v','--view', action='store_true',help='View folder of selected section')
parser.add_argument('-p','--play', action='store_true',help='Play video files of selected section ')
parser.add_argument('-t','--time', action='store_true',help='View watched time of course and other infos (use with -s)')
args = parser.parse_args()


MI = MediaInfo()

colors = [Fore.LIGHTYELLOW_EX,Fore.LIGHTMAGENTA_EX]

sections = []


class Section:
    
    numOfVideos = 0
    videosLength = ()
    videoMillis = 0
    
    def __init__(self,title,path,files,color):
        
        self.title = title
        self.path = path
        self.color = color
        self.files = files
        
    def __str__(self):
        
        placeholder = ""
        line = "-"*80+"\n"
        
        if self.videosLength == 1:
            placeholder = "video" 
        else:
            placeholder = "videos"
        
        
        msg = self.color + '{line}|\t{self.title}\n|\n| Total length of videos is  {time}\n| This section has {self.numOfVideos} {placeholder}.\n| Average length of video is {avg}\n{line}'.format(self=self,placeholder = placeholder,time = getTimeMsg(self.videosLength),avg = getTimeMsg(self.getAvg()),line = line)
        
        return msg
    
    
    def getAvg(self):
        
        if self.numOfVideos !=0:
            return convert_from_ms(int(self.videoMillis/self.numOfVideos))
        return(0,0,0,0)
    


def jsonToSections(inputData):
    
    keys = inputData[0].keys()
    jsonData = json.dumps(inputData[0])
    json1_data = json.loads(jsonData)
    
    for key in keys:
        new_section = Section(
            json1_data[key][0]['title'],
            json1_data[key][0]['path'],
            json1_data[key][0]['files'],
            json1_data[key][0]['color']
        )
        new_section.numOfVideos = json1_data[key][0]['numOfVideos']
        new_section.videosLength = json1_data[key][0]['videosLength']
        new_section.videoMillis = json1_data[key][0]['videoMillis']
             
        
        
        sections.append(new_section)


def watchedVideosInfo():
    line = "="*80+"\n"
    fullVideosMillis,fullVideosCount = getVideosInfo()
    videosMillis,videosCount = getVideosInfo(args.section-1)
    timeLeftMillis = fullVideosMillis - videosMillis
    
    watchedTime = convert_from_ms(videosMillis)
    watchedTimeMsg = getTimeMsg(watchedTime)
    
    timeLeft = convert_from_ms(timeLeftMillis)
    timeLeftMsg = getTimeMsg(timeLeft)
    
    
    
    print(Fore.WHITE+line)
    print(Fore.CYAN + 'Info:')
    
    print(Fore.LIGHTRED_EX+'\tSection {} of {} and you watched {} of course.'.format(args.section,len(sections),watchedTimeMsg))
    print(Fore.LIGHTRED_EX+'\tYou watched {} of {} videos and that is {}% of course.'.format( videosCount, fullVideosCount, round((videosCount/fullVideosCount)*100)) )
    print(Fore.LIGHTRED_EX+'\tTime left to finish course is: {} \n'.format(timeLeftMsg))
    
    print(Fore.WHITE+line)
     
     
       
    
    
    
def getVideosInfo(end=0):
    if(end == 0):
        end = len(sections)
    
        
    videosMillis = 0
    videosCount = 0
    
    for i in range(end):
        
        videosMillis += sections[i].videoMillis
        videosCount += sections[i].numOfVideos
    
    return (videosMillis,videosCount)
    
      
    
def allSectionsInfos():
    
    videosMillis,videosCount = getVideosInfo()
    
    
    videosLength = 0
    videosLengthMsg = ""
    totalSections = len(sections)
    line = "*"*80+"\n"
    
    
        
    videosLength = convert_from_ms(videosMillis)
    videosLengthMsg = getTimeMsg(videosLength)
    avgVideosMsg = ""
    
    if videosCount !=0:
        avgVideosLength = convert_from_ms(int(videosMillis/videosCount))
        avgVideosMsg = getTimeMsg(avgVideosLength)
    
    
    print(Fore.LIGHTRED_EX+'\n\n{line}\t\tTotal sections in this Course is: {total}\n\t\tTotal length of all videos is: {time}\n\t\tTotal number of all videos is: {videosCount}\n\t\tAverage length of videos is: {avg}\n{line}\n'.format(total = totalSections,line = line,time=videosLengthMsg,videosCount=videosCount,avg = avgVideosMsg))
    
    
def getTimeMsg(time):
    
    msgs = []
    timeMsg=""
    
    if time[0] > 0:
        msgs.append(str(time[0])+ "d ")
    if time[1] > 0 or time[0] > 0 :
        msgs.append(str(time[1]) + "h ")
    if time[2] > 0 or time[1] > 0:
        msgs.append(str(time[2]) + "m ")
    if time[3] > 0 or time[2] > 0:
        msgs.append(str(round(time[3],1))+"s")
    return timeMsg.join(msgs)


def openFolder(path):
    
    time.sleep(0.5)
    webbrowser.open(path)
    time.sleep(1.5)
    
def playVideos(section):
    
    videoPaths = []
    files = section.files
    path = section.path
        
    for file in files:
        root_ext = os.path.splitext(file)
        if root_ext[1] not in allowed_ext:
            continue
        videoPaths.append(fixPath(path)+file)
        
    command = [videoPlayer]
        
    command+= videoPaths
        
    p = subprocess.Popen(command)



def printOneSection():
    
    print(sections[0])
    
    if args.view:
        openFolder(sections[0].path)
    
    if args.play:
        playVideos(sections[0])
        
        
               
def printNsection(num):
    
    num -= 1
    length = len(sections)
    
    if num >= 0 and num < length:
        print(sections[num])
        if args.time:
            watchedVideosInfo()
        if args.view:
            openFolder(sections[num].path)
        
        if args.play:
            playVideos(sections[num])
    else:
        print(Fore.RED+'Can\'t find that section sir! ')
        
    
    
          
def printAllSections():
    
    for sect in sections:
        print(sect)
    

def addSectionsInfo():
    
    for sect in sections:
        addInfo(sect)


def addInfo(section):
    
    path = fixPath(section.path)
    millis = sum(get_lengths_in_milliseconds_of_directory(path,section))
    section.videosLength = convert_from_ms(millis)
    section.videoMillis = millis



def walklevel(some_dir, level=1):
    
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    
    
    
    for root, dirs, files in os.walk(some_dir):
        
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]



def getSections(inputPath):
    
    sectionDict = []
    passFirst = 0
    
    for root, dirs,files in walklevel(inputPath,1):
        
        if not args.one:
            
            if passFirst == 0:
                passFirst+=1
                
                continue
            else:
               
                sectionDict.append({
                    "title":root.split(os.path.sep)[-1],
                    "path":root,
                    "files":files
                })
        else:
            
            passFirst+=1
            sectionDict.append({
                "title":root.split(os.path.sep)[-1],
                "path":root,
                "files":files,
            })
       
        
    
    color = colors[0]
    
    for sect in sectionDict:
        r = random.randint(0,1)
        if r:
            color = colors[0]
        else:
            color = colors[1]
       
        new_section = Section(sect["title"],sect["path"],sect["files"],color)
        sections.append(new_section)
        
    
    
    
  
    
    
 
    
def fixPath(inputPath):
    
    path = inputPath.replace("\\","\\\\")+"\\\\"
    return path


def convert_from_ms( milliseconds ):
	
    seconds, milliseconds = divmod(milliseconds,1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    seconds = seconds + milliseconds/1000
    return days, hours, minutes, seconds


def get_lengths_in_milliseconds_of_directory(prefix,section):
    
   
   numOfVideos = 0
   
   for f in os.listdir(prefix):
    root_ext = os.path.splitext(f)
    if root_ext[1] not in allowed_ext:
        continue
    
    
    MI.Open(prefix + f)
    duration_string = MI.Get(Stream.Video, 0, "Duration")
    

    try:
      duration = int(duration_string)
      yield duration
      numOfVideos+=1
      
    except ValueError:
      print("{} is not video file!".format(f))

    MI.Close()
    section.numOfVideos = numOfVideos


def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    float regex comes from https://stackoverflow.com/a/12643073/190597
    '''
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]
    

def main():
    
    
    isInJson = False
    inputData = None
    global sections
    try:
        #location of saved data, change "path" to your folder location 
        with open('"path"\\data.txt') as json_file:
            inputData = json.load(json_file)
            keys = inputData.keys()
            key = args.Path
            
            if(key in keys):
                isInJson = True
            
    except:
        print('File not found maybe this is first scan!')
            
   
   
    
    if isInJson is False:
        getSections(args.Path)
        addSectionsInfo()
        
        sortedTitles = []
        for s in sections:
            sortedTitles.append(s.title)
        
        sortedTitles.sort(key=natural_keys)
       
        
        sortedSections = []
        
        for st in sortedTitles:
            for s in sections:
                if s.title == st:
                    sortedSections.append(s)
                
        sections = sortedSections
        
       
        
        outputData = None
        
        if inputData is None:        
            outputData = {}
            
        else:
            outputData = {}
            outputData.update(inputData)
            
        
        outputData[args.Path] = []
        sectionData = {}
        
        
        for i in range(len(sections)):
            sectTitle = 'Section '+str(i+1)
            
            sectionData[sectTitle] = []
            sectionData[sectTitle].append({
                
                    
                    'numOfVideos':sections[i].numOfVideos,
                    'videosLength':sections[i].videosLength,
                    'videoMillis':sections[i].videoMillis,
                    'title':sections[i].title,
                    'path':sections[i].path,
                    'color':sections[i].color,
                    'files':sections[i].files
                
            })
        outputData[args.Path].append(sectionData)
        #location where we save data, replace "path" with your folder location
        with open('"path"\\data.txt','w') as outfile:
            json.dump(outputData,outfile)
    else:
        
        jsonToSections(inputData[args.Path])
        
        
            
        
    if args.section == -1 and not args.one:
        printAllSections()
    elif args.one:
            printOneSection()
    else:
        printNsection(args.section)
            
    if not args.one and args.section == -1:
        allSectionsInfos()
    
    
    
    
    
if __name__== "__main__":
   
    start_time = time.time()
    main()
  
    print(Fore.LIGHTBLUE_EX+"Execution time --- %s seconds ---" % (time.time() - start_time))


