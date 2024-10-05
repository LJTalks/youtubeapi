from django.shortcuts import render
import requests
import os
from datetime import datetime


YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = 'https://www.googleapis.com/youtube/v3/'


# Helper function to fetch videos from a YouTube channel
def get_videos_from_channel(channel_id):
    url = f'{BASE_URL}search?key={YOUTUBE_API_KEY}&channelId={
        channel_id}&part=snippet,id&order=date&maxResults=50'
    print(f"Fetching videos from channel: {channel_id}")
    print(f"API URL: {url}")  # Debugging URL to make sure it's correct
    response = requests.get(url)
    print(f"Response status: {response.status_code}")  # DEBUG
    if response.status_code == 200:
        videos = response.json().get('items', [])
        return videos
    else:
        print(f"Error fetching videos: {response.content}")  # DEBUG
        return []


# Helper function to get video details (statistics and snippet)
def get_video_details(video_id):
    url = f'{BASE_URL}videos?key={YOUTUBE_API_KEY}&id={
        video_id}&part=statistics,snippet'
    print(f"Fetching video details for video ID: {video_id}")
    response = requests.get(url)
    print(f"Error fetching video details: {response.content}")  # DEBUG
    if response.status_code == 200:
        return response.json().get('items', [])[0]
    else:
        print(f"Error fetching video details: {response.content}")  # DEBUG
        return {}


# Main view to handle form submission and display data
def fetch_data(request):
    video_details_list = []  # Initialize an empty list for the videos
    
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id')
        sort_by = request.POST.get('sort_by')
        
        print(f"Channel ID received: {channel_id}")
        videos = get_videos_from_channel(channel_id)
        
        # Fetch detailed info for each video
        for video in videos:
            video_id = video['id'].get('videoId')
            if video_id:  # Check if video_id exists before proceeding
                video_details = get_video_details(video_id)
                
                # Calculate days since published
                published_at = video_details['snippet']['publishedAt']
                published_date = datetime.strptime(
                    published_at, '%Y-%m-%dT%H:%M:%SZ')
                formatted_published_date = published_date.strftime(
                    '%d/%m/%y %H:%M')
                
                days_since_published = (datetime.now() - published_date).days
                
                # Calculate engagement percentage
                views = int(video_details['statistics']['viewCount'])
                likes = int(video_details['statistics']['likeCount'])
                comments = int(video_details[
                    'statistics'].get('commentCount', 0))
                
                if views > 0:  # Prevent division by 0
                    likes_to_views = (likes / views) * 100
                    comments_to_views = (comments / views) * 100
                    total_engagement_rate = ((likes + comments) / views) * 100
                else:
                    likes_to_views = 0
                    comments_to_views = 0 
                    total_engagement_rate = 0
                    
                # Add calculated metrics to the video details
                video_details[
                    'formatted_published_date'] = formatted_published_date
                video_details['days_since_published'] = days_since_published
                video_details['likes_to_views'] = likes_to_views
                video_details['comments_to_views'] = comments_to_views
                video_details['total_engagement_rate'] = total_engagement_rate
                
                # Append the video details to the list (only once) 
                video_details_list.append(video_details)
                
        # Sorting logic
        if sort_by == 'date':
            video_details_list.sort(key=lambda x: x[
                'snippet']['publishedAt'], reverse=True)
        elif sort_by == 'views':
            video_details_list.sort(key=lambda x: int(
                x['statistics']['viewCount']), reverse=True)
        elif sort_by == 'engagement_rate':
            video_details_list.sort(key=lambda x: x[
                'engagement_rate'], reverse=True)

    # Pass the video details to front-end for display
    context = {'video_details_list': video_details_list}
    return render(request, 'ytinfo/yt_main.html', context)
