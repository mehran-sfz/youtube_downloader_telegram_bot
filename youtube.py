import scrapetube
import requests
from bs4 import BeautifulSoup
from pytube import YouTube


def find_channel_id(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        metas = soup.find_all('meta')
        for meta in metas:
            if meta.get('itemprop') == 'channelId':
                return(meta['content'])
            else:
                return(0)
    except:
        return(0)

def get_videos_from_channel(id):
    try:
        videos = scrapetube.get_channel(id)
        urls = []
        counter = 0
        for video in videos:
            url = f"https://www.youtube.com/watch?v={video['videoId']}"
            title = {video['title']['runs'][0]['text']}
            urls.append({'url' : url, 'title' : title, 'counter' : counter})
            counter += 1
        return(urls)
    except:
        return(0)

def find_videos_with_search(word, number):
    urls = []
    counter = 1
    try:
        videos = scrapetube.get_search(word)

        for video in videos:
            url = f"https://www.youtube.com/watch?v={video['videoId']}"
            title = {video['title']['runs'][0]['text']}
            urls.append({'url' : url, 'title' : title, 'counter' : counter})
            
            counter += 1
            if counter == int(number):
                return(urls)
        return(urls)
    except:
        return(0)

def Download(link, user_id):
    try:
        yt = YouTube(link)
        yt = yt.streams.filter(res = '720p', only_audio = False, file_extension = 'mp4', progressive = True)
        if yt:
            status = yt[0].download(f'Downloads/{user_id}')
            return(status)
        else:
            return(0)
    except:
        return(0)
