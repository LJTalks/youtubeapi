import requests
import json

API_KEY = "AIzaSyA-94XofldblPLc8B2tjJVpx2aUQMZDuyw"
CHANNEL_ID = "UCUYiR0vMGLP6bgU-4N9S6bw"
BASE_URL = 'https://www.googleapis.com/youtube/v3/'

# Do we want to restrict comments to 50?
def get_videos_from_channel(channel_id):
    url = f'{BASE_URL}search?key={API_KEY}&channelId={channelId={channel_id}&part=snippet},id&order=date&maxResults=50'
    response = requests.get(url)
    videos = response.json().get('items', [])
    return videos

def get_video_details(video_id):
    url = f'{BASE_URL}videos?key={API_KEY}&id={video_id}&part=statistics, snippet'
    response = requests.get(url)
    return response.json().get('items', [])[0]

# Example usage
videos = get_videos_from_channel(CHANNEL_ID)
for video in videos:
    video_id = video['id'][video_id]
    video_details = get_video_details(video_id)
    print(video_details)
    