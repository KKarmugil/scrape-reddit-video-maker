from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import configparser
import praw
import pandas as pd
from gtts import gTTS
import librosa
import re
import os
from tqdm import tqdm ,trange
import pyttsx3 
import logging
#subredditTep = input("Exp AskReddit, explainlikeimfive ")
kim=0
subredditTep = "explainlikeimfive"
csvRead = ""
clip = ""
addw = 8
commentname = {}
numberOfPost = ""
audiocon = 0
cliptime = {}
addedline={}
texttemp=""
endtext={}
audioTime=0
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

path = (os.path.dirname(os.path.abspath(__file__)))
path=path.capitalize()
path=(path.replace('\\', '\\\\'))
path=(path+"\\\\")
#print (path)
rawtext={}
try:
    os.mkdir(path+"temp")
except:
    print("already created")
try:
    os.mkdir(path+"result")
except:
    print("already created")


# Creates Config File

config = configparser.ConfigParser()

try:
    config.read("configfile.ini")
    readredditinfo = config["redditinfo"]
    user = readredditinfo["client_id"]
    password = readredditinfo["client_secret"]
    host = readredditinfo["user_agent"]
except:
    # Add the structure to the file we will create
    config.add_section('redditinfo')
    config.set('redditinfo', 'client_id', input("Enter client_id : "))
    config.set('redditinfo', 'client_secret', input("Enter client_secret : "))
    config.set('redditinfo', 'user_agent', input("Enter user_agent : "))

    with open("configfile.ini", 'w') as configfile:
        config.write(configfile)

    config.read("configfile.ini")
    readredditinfo = config["redditinfo"]
    user = readredditinfo["client_id"]
    password = readredditinfo["client_secret"]
    host = readredditinfo["user_agent"]


def redditpull():
    subredditTep=input("Exp AskReddit, explainlikeimfive ")
    global numberOfPost
    numberOfPost = int(input("Enter Number Of Posts :"))
    reddit = praw.Reddit(client_id=user,
                         # your client id
                         client_secret=password,
                         # your client secret
                         user_agent=host)
    posts = []
    ml_subreddit = reddit.subreddit(subredditTep)
    with tqdm(total=int(numberOfPost*5)) as pbar:
        for post in ml_subreddit.top("day", limit=numberOfPost):
            for i in trange(5):
                comment_id = post.comments[i].id
                comment = reddit.comment(comment_id)
                commentname[i] = comment.author
                pbar.update(1)
            posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created, post.comments[0].body, post.comments[1].body,
                         post.comments[2].body, post.comments[3].body, post.comments[4].body, commentname[0], commentname[1], commentname[2], commentname[3], commentname[4]])
    posts = pd.DataFrame(posts, columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body',
                         'created', 'top_comment', 'two', 'three', 'four', 'five', 'id1', 'id2', 'id3', 'id4', 'id5'])
    try:
        posts.to_csv(r'temp\file3.csv')
    except:
        print("Close the Csv file and then run again")

# Read Csv File


def readfile(row, column):
    df = pd.read_csv(r'temp\file3.csv')
    return df.loc[row][column]

def textsplit(text):
    tempstore={}
    tem1=0
    tem2=50
    countOfWords = text.split()
    #print(len(countOfWords))
    #print("Count of Words in the given Sentence:", countOfWords)
    cal=int(len(countOfWords)/50)
    cal=cal+1
    for i in trange(cal):
        tempstore[i]=countOfWords[tem1:tem2]
        tem1=tem1+50
        tem2=tem2+50
    return(tempstore)

def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele+" "
 
    return str1

def textdived(text):
    text=re.sub("ELI5: ", "", text)
    text=re.sub('[?,:,!]', "", text)
    global outputname,rawtext
    lens=0+len(rawtext)
    mm=textsplit(text)
    
    for i in mm:
        rawtext[lens]=listToString(mm[i])
        lens=lens+1
    outputname=re.sub('[?,\',/,$,ELI5:,!]', '', rawtext[0])
    outputname=re.sub("ELI5: ", '', outputname)
    # outputname=re.sub("ELI5: ", "", outputname)
    # outputname =re.sub("!", "", outputname)

def audioconveter(text,i):
    mytext = text
    
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("temp\\name"+str(i)+".mp3")
    # except:
    #     engine = pyttsx3.init('sapi5')
    #     engine.save_to_file(mytext , "temp\\name"+str(i)+".mp3")
    #     engine.runAndWait()

def order(text,kgf):
    global mk
    mary = text
    mk=[]
    kk=0
    ma=mary.split() 
    mx=len(ma)
    while True:
        if mx%4 == 0:
            break
        else:
            ma.append(" ")
            mx=len(ma)
    cals=int(mx/4)
    for i in trange(cals):
        z=ma[kk]+" "+ma[kk+1]+" "+ma[kk+2] +" "+ma[kk+3] +"\n"
        kk=kk+4
        mk.append(z)
    addedline[kgf]=mk
    #print(addedline)
    subanswer(kgf)

def subanswer(i):
    global texttemp
    file1 = open("temp\\"+"a"+str(i)+".txt", "w")
    file1.writelines(addedline[i])
    file1.close()

def color_clip(size, duration, fps=25, color=(0, 0, 0)):
    global clip
    clip = ColorClip(size, color, duration=duration)

def audiotime():
    for i in cliptime:
        audiotime=audiotime+cliptime[i]
    #print(audiotime)



def videoz():
    global cliptime,rawtext,kim,mk,texttemp,addedline
    for i in trange(len(cliptime)-1):
        m=i+1
        cliptime[m]=cliptime[i]+cliptime[m]
        #print(cliptime[i])
    audioTime=cliptime[len(cliptime)-1]
    #print(audioTime)
    for i in trange(len(addedline)):
        with open("temp\\"+"a"+str(i)+".txt") as f:
         endtext[i] = f.read()
    
    #print(endtext)
    size = (1080, 1920)
    duration = audioTime
    color_clip(size, duration)
    global subredditTep
    jip = "r/"+subredditTep
    txt0_clip = TextClip(jip, fontsize=40, color='white')
    txt0_clip = txt0_clip.set_pos((0.1, 0.1), relative=True).set_duration(duration)
    generator = lambda txt: TextClip(txt, font='Arial', fontsize=40, color='white')
    subs = [((0, cliptime[0]), endtext[0])]
    #print(addedline)
    for i in trange(int(len(addedline)-1)):
        m=i+1
        #print(i)
        subs.append(((cliptime[i],cliptime[m]), endtext[m]))
        #print(subs)
    #print("pass")
    #print(subs)
    subtitles = SubtitlesClip(subs, generator)
    video = CompositeVideoClip(
        [clip,txt0_clip, subtitles.set_pos(('center'))])
    cam=[]
    for i in trange(len(addedline)):
        cam.append(AudioFileClip('temp\\'+"name"+str(i)+".mp3"))
    #print(cam)
    rawtext={}
    mk={}
    texttemp={}
    cliptime = {}
    addedline={}
    fin=concatenate_audioclips(cam)
    fin.write_audiofile("ouut.mp3")
    
    #print(rawtext)
    #print(mk)
    try:
        video.write_videofile("result\\"+str(outputname)+
                            ".mp4",threads=4, fps=25, audio="ouut.mp3")
    except:
        print(outputname+"Error")
    kim=kim+1
    

redditpull()

for j in trange(20):
    textdived(readfile(j, 1))
    textdived(readfile(j, 9))

    for i in rawtext:
        audioconveter(rawtext[i],i)
        order(rawtext[i],i)
        ten = librosa.get_duration(filename="temp\\name"+str(i)+".mp3")
        cliptime[i] = ten
    videoz()
    print("__SUCCESS"+str(j))
    logger.error("done "+str(j))


