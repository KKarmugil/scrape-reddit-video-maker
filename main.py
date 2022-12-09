import praw
import json
from moviepy.editor import *
import time
import textwrap
from gtts import gTTS
import librosa
import re
import random
import os
import configparser


txt_clip = []
endtime = 0
audioclipname = []

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

# Format text in 50px
def videoprep(input, starts, ends, position):
    global txt_clip
    input = textwrap.fill(input, width=45)
    txt_clip.append(TextClip(input, fontsize=40, font="Malgun-Gothic-Bold",
                    color='white').set_pos(position).set_start(starts).set_end(ends))


def vedios(videoOutputName):
    clip = VideoFileClip(backgroundVideo)
    length = clip.duration
    while True:
        # Generate a random floating-point number between 1.0 and 10.0
        random_number = random.uniform(10.0, length)
        # Print the generated random number
        random_number_end = random_number+endtime
        print(1)
        if random_number_end <= length:
            print(random_number)
            print(random_number_end)
            break

    # Create a new video clip with a black background
    videos = ColorClip(size=(1080, 1920), color=(
        0, 0, 0)).set_duration(endtime)
    video = VideoFileClip(backgroundVideo).subclip(
        random_number, random_number_end).set_duration(endtime).set_pos("center")
    image_clip = ImageClip("bg.png").set_duration(endtime)
    video = video.resize(2.0)
    # Create a TextClip with the text that you want to overlay on the video
    raw = [videos, video, image_clip, TextClip(
        "r/"+subreddit_name, fontsize=40, font="Malgun-Gothic-Bold", color='white').set_pos((50, 70)).set_start(0).set_end(endtime)]
    for i in txt_clip:
        raw.append(i)
    rawaudio = []
    for i in audioclipname:
        rawaudio.append(AudioFileClip(i))
    combainaudio = concatenate_audioclips(rawaudio)
    combainaudio.write_audiofile("combainaudio.mp3")
    # Overlay the text clip on the video
    final_clip = CompositeVideoClip(raw)

    # Save the video clip to a file
    final_clip.write_videofile(
        videoOutputName+".mp4", fps=24, audio="combainaudio.mp3")


def reddit_api(subreddit_name, num_posts):
    # Create an instance of the Reddit API
    reddit = praw.Reddit(client_id=user,
                         client_secret=password,
                         user_agent=host)

    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.top(time_filter="day", limit=num_posts)

    # Use a list to store the dictionaries for each post
    post_data = []

    # Print the title and score of each post
    for i, post in enumerate(posts):
        # Create a dictionary for the current post
        post_dict = {
            "title": post.title,
            "post_score": post.score,
            "post_username": str(post.author),
            "comments": [],
            "comment_scores": [],
            "comment_usernames": []
        }

        # Extract the data from the post's comments
        comments = post.comments[:5]
        for comment in comments:
            post_dict["comments"].append(comment.body)
            post_dict["comment_scores"].append(comment.score)
            post_dict["comment_usernames"].append(str(comment.author))

        # Add the post dictionary to the list of post dictionaries
        post_data.append(post_dict)

        progress = (i + 1) / num_posts * 100
        print(f"\rProgress: {progress:.1f}%", end="")

    return post_data


def write_json(data, filename):
    with open(filename + ".json", "w") as file:
        # Use json.dumps to encode the dictionary as a JSON string
        json_string = json.dumps(data)
        # Write the JSON string to the file
        file.write(json_string)


def read_json(filename):
    with open(filename + ".json", "r") as file:
        # Read the JSON string from the file
        json_string = file.read()
        # Use json.loads to decode the JSON string and recreate the dictionary
        data = json.loads(json_string)
        return data


# Set the text to be converted to speech
# Convert the text to speech and save the output to an MP3 file
def tta(inputText, outputname):
    language = "en"
    tts = gTTS(text=inputText, lang=language, slow=False)
    filenames = str(outputname)+".mp3"
    tts.save(filenames)
    duration = librosa.get_duration(filename=filenames)
    audioclipname.append(filenames)
    return (duration)


def aavc(content, username, postscore):
    global starttimes, endtime
    starttimes = endtime
    endtime = tta(content, endtime)+starttimes
    videoprep(content, starttimes, endtime, 'center')
    videoprep(username, starttimes, endtime, (100, 200))
    videoprep(postscore, starttimes, endtime, (100, 1700))

def cleanup():
    # Use the __file__ variable to get the path of the current script
    script_path = __file__

    # Use the os.path.dirname function to get the parent directory of the script
    script_dir = os.path.dirname(script_path)
    folder_path = script_dir

    # Define the path to the folder

    # Use the os.listdir function to get a list of files in the folder
    files = os.listdir(folder_path)

    # Use a for loop to iterate over the files
    for file in files:
        # Use the os.path.splitext function to split the file name and extension
        name, ext = os.path.splitext(file)

        # If the file has a .mp3 or .txt extension, delete it
        if ext == ".mp3" or ext == ".txt":
            os.remove(os.path.join(folder_path, file))


# Use the functions to retrieve data from Reddit and write it to a JSON file
subreddit_name = input("Subreddit (Default [AskReddit]) :- ")or "AskReddit"
num_posts = input("Number Of Post (Default [30]) :- ")or 30
backgroundVideo=input("backgroundVideo Name (Default [bg.mp4]) :- ") or "bg.mp4"
data = reddit_api(subreddit_name, int(num_posts))
write_json(data, "reddit_data")

# Read the data back from the JSON file
data = read_json("reddit_data")
start = time.time()
print("\nstart")
for j in range(len(data)):
    aavc(data[j]["title"], "u/"+data[j]["post_username"],
         "^ " + str(data[j]["post_score"]))
    for i in range(len(data[j]["comments"])):
        aavc(data[j]["comments"][i], "u/"+data[j]["comment_usernames"]
             [i], "^ "+str(data[j]["comment_scores"][i]))
    title = re.sub(r"[^\w\s]", "", data[j]["title"])
    vedios(title)
    txt_clip = []
    endtime = 0
    audioclipname = []
end = time.time()
end = end-start
print(end)
cleanup()
input("PRESS ENTER")
