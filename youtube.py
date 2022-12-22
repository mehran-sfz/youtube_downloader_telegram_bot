import scrapetube
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import os


def find_channel_id(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    metas = soup.find_all('meta')
    for meta in metas:
        if meta.get('itemprop') == 'channelId':
            return(meta['content'])


def get_videos_from_channel(id):
    videos = scrapetube.get_channel(id)
    urls = []
    counter = 0
    for video in videos:
        url = f"https://www.youtube.com/watch?v={video['videoId']}"
        title = {video['title']['runs'][0]['text']}
        urls.append({'url' : url, 'title' : title, 'counter' : counter})
        counter += 1
    return(urls)

def find_videos_with_search(word, number):
    urls = []
    counter = 1
    videos = scrapetube.get_search(word)

    for video in videos:
        url = f"https://www.youtube.com/watch?v={video['videoId']}"
        title = {video['title']['runs'][0]['text']}
        urls.append({'url' : url, 'title' : title, 'counter' : counter})
        
        counter += 1
        if counter == int(number):
            return(urls)
    return(urls)



def Download(link):
    try:
        yt = YouTube(link)
        yt = yt.streams.filter(res = '720p', only_audio = False, file_extension = 'mp4', progressive = True)
        if yt:
            yt[0].download('downloads')
            return('good')
        else:
            return('not good quality')
    except:
        return('bad')




def main():

    text = '''
    a) download with search ?
    b) download with channel url ?'''

    ans = input(text)
    if ans == 'a':

        counter = int(input('enter number of videos you want to download :'))
        word = input('Enter the woed that you wanna search :')
        print(f'you want download {counter} of {word}')
        ok = input('if it is ok enter Yes[Y] :')

        if ok.lower() == 'yes' or ok.lower() == 'y':
            urls = find_videos_with_search(word, counter)

            list_of_videos = os.listdir('downloads')

            for url in urls:
                if f"{url['title']}.mp4" in list_of_videos:
                    status = Download(url['url'])
                    print(f"{url['counter']} - {status}, for video {url['title']}")
                else:
                    continue

        else:
            return(main())

    elif ans == 'b':

        url = input('Enter the url of channel you wanna download :')
        ok = input('if it is ok enter Yes[Y] :')

        if ok.lower() == 'yes' or ok.lower() == 'y':
            id = find_channel_id(url)
            urls = get_videos_from_channel(id)
            print(f'there is {len(urls)} videos on channel.')

            for url in urls:
                if f"{url['title']}.mp4" in list_of_videos:
                    status = Download(url['url'])
                    print(f"{url['counter']} - {status}, for video {url['title']}")
                else:
                    continue

        else:
            return(main())
    
    else:
        return(main())

