import sys
import json
import urllib.request
from pytube import YouTube

def usage():
    pass

def fetch_video_list(api_key, cid):
    base_video_url = 'https://www.youtube.com/watch?v='    
    base_search_url = (
        'https://www.googleapis.com/youtube/v3/search?'
        'key=%s&channelId=%s&part=snippet,id&order=date'
        '&maxResults=25&pageToken=%s'
    )

    vlist = []
    url = base_search_url % (api_key, cid, '')
    while True:
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)
        
        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                vlist.append(base_video_url + i['id']['videoId'])

        break
                
        try:
            next_page_token = resp['nextPageToken']
            url = base_search_url % (api_key, cid, next_page_token)
        except:
            break    

    return vlist
    

if __name__ == '__main__':    
    if len(sys.argv) < 3:
        usage()
        exit()
        
    api_key, cid = sys.argv[1:]

    vlist = fetch_video_list(api_key, cid)
    for vname in vlist:
        print(vname)
        
        yt = YouTube(vname)
        yt.streams[0].download(output_path='results')       
