import sys
import json
import urllib.request
from pytube import YouTube


class Fetcher:
    def __init__(self, api_key, cid):
        self._base_url = (
            'https://www.googleapis.com/youtube/v3/search?'
            'key=%s&channelId=%s&part=snippet,id&order=date'
            '&maxResults=50'
        ) % (api_key, cid)
        
    def __iter__(self):
        url = self._base_url
        # TODO: wh
        while True:
            inp = urllib.request.urlopen(url)
            resp = json.load(inp)
            
            for i in resp['items']:
                if i['id']['kind'] == "youtube#video":
                    yield i['id']['videoId']
                else:
                    print(i['id']['kind'])
                   
            #break # TODO: quota exceed
            try:
                next_page_token = resp['nextPageToken']
                url = self._base_url + '&pageToken=%s' % next_page_token
            except:
                raise StopIteration    

def usage():
    pass


if __name__ == '__main__':    
    if len(sys.argv) < 3:
        usage()
        exit()
        
    api_key, cid = sys.argv[1:]

    base_video_url = 'https://www.youtube.com/watch?v='
    
    l = 0
    for vname in Fetcher(api_key, cid):
        print('https://www.youtube.com/watch?v=' + vname)
        l += 1
        try:
            yt = YouTube('https://www.youtube.com/watch?v=' + vname)
            stream = yt.streams.filter(mime_type='video/mp4').order_by('resolution').desc().first()            
            stream.download(output_path='results')       
        except:
            print('FAIL: https://www.youtube.com/watch?v=' + vname)
    print(l)