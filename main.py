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
commentname = {}
cliptime = {}
path = (os.path.dirname(os.path.abspath(__file__)))
path=path.capitalize()
path=(path.replace('\\', '\\\\'))
path=(path+"\\\\")
print (path)
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
    subredditTep= readredditinfo["subreddit"]
except:
    # Add the structure to the file we will create
    config.add_section('redditinfo')
    config.set('redditinfo', 'client_id', input("Enter client_id : "))
    config.set('redditinfo', 'client_secret', input("Enter client_secret : "))
    config.set('redditinfo', 'user_agent', input("Enter user_agent : "))
    config.set('redditinfo', 'subreddit', input("Enter subreddit E.g AskReddit, askscience.. : "))


    with open("configfile.ini", 'w') as configfile:
        config.write(configfile)

    config.read("configfile.ini")
    readredditinfo = config["redditinfo"]
    user = readredditinfo["client_id"]
    password = readredditinfo["client_secret"]
    host = readredditinfo["user_agent"]
    subredditTep= readredditinfo["subreddit"]


# Gets Info From reddit and Store in Csv File

def redditpull():
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
            for i in range(5):
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

# Text To Audio


def audiocon(name):
    global csvRead
    mytext = csvRead
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save(name+".mp3")


def audiocon1():
    global csvRead
    mytext = csvRead
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save(r"temp\name"+".mp3")


def allaudio(row, col=1):
    global csvRead
    global audiocon
    global outputname
    for i in trange(6):
        if col == 1:
            combain = 'temp\\'+str(row)+"_"+str(col)
            csvRead = readfile(row, col)
            outputname=re.sub('[[,:,?,\',/,\]]', '', csvRead)
            question()
            audiocon(combain)
            audioTime = librosa.get_duration(filename=combain+'.mp3')
            cliptime[i] = audioTime
            order(i)
            col = col+7
        elif col <= 12:
            col = col+1
            combain = 'temp\\'+str(row)+"_"+str(col)
            csvRead = readfile(row, col)
            answer()
            audiocon(combain)
            temp = librosa.get_duration(filename=combain+'.mp3')
            audioTime = audioTime+temp
            cliptime[i] = audioTime
            order(i)
        else:
            break
    with open('temp\\'+"myfile.txt") as f:
        csvRead = f.read()
    audiocon1()
    videoz()

def order(arr):
    global texttemp
    mary = csvRead
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
    for i in range(cals):
        z=ma[kk]+" "+ma[kk+1]+" "+ma[kk+2] +" "+ma[kk+3] +"\n"
        kk=kk+4
        mk.append(z)
    texttemp=mk
    subanswer(arr)

def subanswer(i):
    global texttemp
    file1 = open("temp\\"+"a"+str(i)+".txt", "w")
    file1.writelines(texttemp)
    file1.close()


def question():
    global csvRead
    mary = csvRead
    file1 = open("temp\\"+"myfile.txt", "w")
    file1.writelines(mary)
    file1.close()


def answer():
    global csvRead
    mary = csvRead
    file1 = open("temp\\"+"myfile.txt", "a")  # append mode
    file1.writelines(mary)
    file1.close()


def color_clip(size, duration, fps=25, color=(0, 0, 0)):
    global clip
    clip = ColorClip(size, color, duration=duration)

# Video render
    
def videoz():
    global clip
    audioTime = librosa.get_duration(filename="temp\\"+'name.mp3')
    with open("temp\\"+"a0.txt") as f:
        text0 = f.read()
    with open("temp\\"+"a1.txt") as f:
        text1 = f.read()
    with open("temp\\"+"a2.txt") as f:
        text2 = f.read()
    with open("temp\\"+"a3.txt") as f:
        text3 = f.read()
    with open("temp\\"+"a4.txt") as f:
        text4 = f.read()
    with open("temp\\"+"a5.txt") as f:
        text5 = f.read()
    size = (1080, 1920)
    duration = audioTime
    color_clip(size, duration)
    global subredditTep
    jip = "r/"+subredditTep
    txt0_clip = TextClip(jip, fontsize=40, color='white')
    txt0_clip = txt0_clip.set_pos((0.1, 0.1), relative=True).set_duration(duration)
    generator = lambda txt: TextClip(txt, font='Arial', fontsize=40, color='white')
    subs = [((0, cliptime[0]), text0),
        ((cliptime[0],cliptime[1]), text1),
        ((cliptime[1],cliptime[2]), text2),
        ((cliptime[2],cliptime[3]), text3),
        ((cliptime[3],cliptime[4]), text4),
        ((cliptime[4],cliptime[5]), text5)]
    subtitles = SubtitlesClip(subs, generator)
    video = CompositeVideoClip(
        [clip,txt0_clip, subtitles.set_pos(('center'))])
    try:
        video.write_videofile("result\\"+str(outputname)+
                            ".mp4", fps=25, audio='temp\\'+"name.mp3")
    except:
        print(outputname+"Error")

def main():
    redditpull()
    global numberOfPost
    for i in range(0,numberOfPost):
        try:
            allaudio(i)
        except:
            print("ERROR "+str(i))

main()


