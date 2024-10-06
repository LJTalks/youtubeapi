from django.shortcuts import render
import requests
import os
from datetime import datetime
import csv
from django.http import HttpResponse
import html
import re


# Function to mask API keys (show only the first and last 4 characters)
def mask_key(key):
    return key[:4] + '*' * (len(key) - 8) + key[-4:]


YOUTUBE_API_KEYS = [os.getenv(
    "YOUTUBE_API_KEY_1"), os.getenv("YOUTUBE_API_KEY_2")]
current_key_index = 0  # Start wit the second key first
YOUTUBE_API_KEY = YOUTUBE_API_KEYS[current_key_index]  # Set initial API key

# Print the masked initial API key to check which one we're starting with
print(f"Starting with API Key: {mask_key(YOUTUBE_API_KEY)}")

BASE_URL = 'https://www.googleapis.com/youtube/v3/'


# Function to switch API keys
def switch_api_key():
    global current_key_index, YOUTUBE_API_KEY
    # Cycle through keys
    current_key_index = (current_key_index + 1) % len(YOUTUBE_API_KEYS)
    # Update global API key
    YOUTUBE_API_KEY = YOUTUBE_API_KEYS[current_key_index]

    # Check which key is currently in use
    print(f"Switched to API Key: {mask_key(YOUTUBE_API_KEY)}")
    return YOUTUBE_API_KEY

    # check which key is currently in use
    print(f"Switching to API Key: {mask_key(YOUTUBE_API_KEY)}")


# Helper function to fetch channel details by channel name
def get_channel_details_by_name(channel_name):
    url = f'{BASE_URL}search?key={YOUTUBE_API_KEY}&q={
        channel_name}&type=channel&part=snippet'
    response = requests.get(url)
    
    if response.status_code == 403 and "quotaExceeded" in response.text:
        print("Quota exceeded, switching API key...")
        switch_api_key()  # Switch the global key
        url = f'{BASE_URL}search?key={YOUTUBE_API_KEY}&q={
            channel_name}&type=channel&part=snippet'
        response = requests.get(url)
        
    if response.status_code == 200:
        channels = response.json().get('items', [])
        if channels:
            return channels[0]  # Return the first channel found
        else:
            print(f"No channels found for {channel_name}")
            return {}
    else:
        print(f"Error fetching channel by name: {response.content}")
        return {}


# Helper function to fetch channel details (e.g., name)
def get_channel_details(channel_id):
    url = f'{BASE_URL}channels?key={YOUTUBE_API_KEY}&id={
        channel_id}&part=snippet'
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
    # print(f"Fetching videos from channel: {channel_id}")  # DEBUG
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
    # print(f"Fetching video details for video ID: {video_id}")  # DEBUG
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

    if request.method == 'POST':
        # Retrieve values from form 
        search_channel_id = request.POST.get('channel_id', '').strip()
        search_channel_name = request.POST.get('channel_name', '').strip()
        # print(f"Channel ID received: {search_channel_id}")
        # print(f"Channel name received: {search_channel_name}")

        # Ensure that either channel name or channel ID is provided
        if not search_channel_id and not search_channel_name:
            return HttpResponse(
                "Please provide either a channel ID nor a Channel Name.")
        
        # print(f"Channel Name entered: {search_channel_name}")
        # print(f"Channel ID entered: {search_channel_id}")
        
        # Search by channel ID if provided
        if search_channel_id:
            # print(f"Fetching data using Channel ID: {search_channel_id}")
            # Fetch channel details by ID
            channel_details = get_channel_details(search_channel_id)
            # print(f"Channel Details (ID): {channel_details}")  # Debugging
            
            channel_name = channel_details.get('snippet', {}).get(
                'title', 'Unknown Channel')
            channel_id = search_channel_id  # Use the ID directly

        # Otherwise, search by channel name if provided
        elif search_channel_name:
            # print(f"Fetching data using Channel Name: {search_channel_name}")
            # Fetch channel details by name
            channel_details = get_channel_details_by_name(search_channel_name)
            # print(f"Channel Details (Name): {channel_details}")  # Debugging
            
            channel_name = channel_details.get('snippet', {}).get(
                'title', 'Unknown Channel')
            channel_id = channel_details.get('id', {}).get('channelId')
            
        # If no channel was found, retun an error
        if not channel_id:
            return HttpResponse(
                f"No channel found for {
                    search_channel_name or search_channel_id}"
            )

        # Fetch videos from the channel
        videos = get_videos_from_channel(channel_id)
        # Fetch detailed info for each video
        for video in videos:
            video_id = video['id'].get('videoId')
            if video_id:  # Check if video_id exists before proceeding
                video_details = get_video_details(video_id)
                
                # Get the comment count from statistics
                comments_count = video_details['statistics'].get(
                    'commentCount', 0)
                
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
                     'Comments', 'Total Engagement %', 'Comments Text'])

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
