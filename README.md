# Scrapes reddit and create videos

## Installation

Install modules specified in requirements.txt

##YOU Need 

1 Client ID

2 Client secret

3 User agent 

To get this three check out this link
https://github.com/reddit-archive/reddit/wiki/OAuth2

Creates videos by scraping information from Reddit and convert to video files
 
It only works with subreddits that are questions and answers type daily top post scrapes the title and top five comments from posts to create a video.

When first time running script it will ask client Id, client secret, user agent and it stores all info to a config file next time running script will not ask any details right now subreddit is default to r/askreddit to change subreddit edit main.py

Enter number of Posts:-

![alt text](https://i.imgur.com/YmWkdaf.png)

Render video and out to a folder called result:-

![alt text](https://i.imgur.com/9vF3e69.png)


