from django.shortcuts import render
import requests
import os
from datetime import datetime
import csv
from django.http import HttpResponse
import html
import re


YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE_URL = 'https://www.googleapis.com/youtube/v3/'


# Helper function to fetch channel details (e.g., name)
def get_channel_details(channel_id):
    url = f'{BASE_URL}channels?key={YOUTUBE_API_KEY}&id={channel_id}&part=snippet'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])[0]
    else:
        print(f"Error fetching channel details: {response.content}")  # DEBUG
        return {}


# Helper function to fetch videos from a YouTube channel
def get_videos_from_channel(channel_id):
    url = f'{BASE_URL}search?key={YOUTUBE_API_KEY}&channelId={
        channel_id}&part=snippet,id&order=date&maxResults=50'
    print(f"Fetching videos from channel: {channel_id}")
    # print(f"API URL: {url}")  # Debugging URL to make sure it's correct
    response = requests.get(url)
    # print(f"Response status: {response.status_code}")  # DEBUG
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
    # print(f"Error fetching video details: {response.content}")  # DEBUG
    if response.status_code == 200:
        return response.json().get('items', [])[0]
    else:
        # print(f"Error fetching video details: {response.content}")  # DEBUG
        return {}


# Main view to handle form submission and display data
def fetch_data(request):
    video_details_list = []  # Initialize an empty list for the videos
    channel_id = None  # Initialise as None
    channel_name = None  # Initialise as None
    # sort_by = None
    # direction = 'asc'  # Default to ascending

    if request.method == 'POST':
        channel_id = request.POST.get('channel_id')
        print(f"Channel ID received: {channel_id}")
        
        # Fetch channel details to get the channel name
        channel_details = get_channel_details(channel_id)
        channel_name = channel_details.get('snippet', {}).get(
            'title', 'Unknown Channel')

        videos = get_videos_from_channel(channel_id)

        # Fetch detailed info for each video
        for video in videos:
            video_id = video['id'].get('videoId')
            if video_id:  # Check if video_id exists before proceeding
                video_details = get_video_details(video_id)
                
                # Get the comment count from statistics
                comments_count= video_details['statistics'].get('commentCount', 0)
                
                # # Fetch the comments for the video
                # comments = fetch_comments(video_id)
                # video_details['comments_list'] = comments

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

        # Store video details in session for CSV export
        request.session['video_details_list'] = video_details_list
        request.session['channel_name'] = channel_name

    # Pass the video details and Channel name to front-end for display
    context = {
        'video_details_list': video_details_list,
        'channel_id': channel_id,
        'channel_name': channel_name
    }

    return render(request, 'ytinfo/yt_main.html', context)


# Helper function to fetch comments for a video
def fetch_comments(video_id):
    url = f'{BASE_URL}commentThreads?key={YOUTUBE_API_KEY}&videoId={
        video_id}&part=snippet&maxResults=50'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return []


# Helper function to remove HTML Tags
def strip_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html.unescape(text))


# New view to export data to CSV
def export_to_csv(request):
    # Retrieve 'video_details_list' and 'channel_name' from session
    video_details_list = request.session.get('video_details_list', [])
    channel_name = request.session.get('channel_name', 'Unknown Channel')

    if not video_details_list:
        return HttpResponse("No data to export.", content_type='text/plain')

    # Create the HTTP response with content type for CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = (
        f'attachment; filename="{channel_name}_youtube_videos.csv"'
    )

    writer = csv.writer(response)
    
    # Write the channel name at the top
    writer.writerow([f"Channel: {channel_name}"])
    writer.writerow([])  # Blank for spacing

    # Write the header row
    writer.writerow(['Title', 'Published At', 'Views', 'Likes',
                     'Comments', 'Engagement Rate', 'Comments Text'])

    # Write data rows
    for video in video_details_list:
        # Fetch the comments for the video
        comments_data = fetch_comments(video['id'])
        comments_text = ' | '.join([strip_html_tags(comment['snippet'][
            'topLevelComment']['snippet'][
                'textDisplay']) for comment in comments_data])

        writer.writerow([
            video['snippet']['title'],
            video['formatted_published_date'],
            video['statistics']['viewCount'],
            video['statistics']['likeCount'],
            video['statistics'].get('CommentCount', 'N/A'),
            f"{video['total_engagement_rate']:.2f}",
            comments_text
        ])

    return response
