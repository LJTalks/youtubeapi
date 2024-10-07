# YouTube Channel Data Fetcher

This project is designed to retrieve video data from a YouTube channel using the YouTube Data API v3.

The data fetched includes video titles, publication dates, view counts, like counts, comment counts, and more.

The app currently fetches video details, including titles, publication dates, view counts, like counts, comment counts, and engagement rates. Users can search for data by inputting a YouTube channel name or channel ID. The data can be exported into a CSV file for further analysis.

This app is in continuous development, with plans to expand its features further, such as storing data in a database for user access and providing additional analytics.

## Current Features

Fetches data for YouTube videos from a user-provided channel name or channel ID.

Calculates and displays engagement metrics, such as likes-to-views and comments-to-views ratios.

Option to export video data to a CSV file for further analysis.

Integrates with the YouTube Data API for fetching real-time data.

## Upcoming Features

Store fetched video information in a PostgreSQL database for better access and future analytics.

A front-end interface where users can log in and store their own channel data for easy access and ongoing analytics.

Provide insights into video performance metrics such as subscriber growth, watch time, and audience demographics (depending on YouTube API limitations).

## Tech Stack

Python: Core programming language.

Django: Web framework to manage the app.

PostgreSQL: Database for storing fetched video data.

Heroku: Deployed on Heroku for live access.

Flake8: Linting and PEP8 compliance.

YouTube Data API: API for retrieving video information.

## Installation

### Prerequisites

Python 3.12+

PostgreSQL

YouTube Data API Key (instructions below)

Heroku CLI

### Clone the Repository

```
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### Set Up Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Requirements

```
pip install -r requirements.txt
```

### Set Up Environment Variables

Create an env.py file in the root of your project.

Add the following environment variables:

python

```
import os

os.environ["YOUTUBE_API_KEY"] = "your_youtube_api_key"

os.environ["DATABASE_URL"] = "postgres://your_username:your_password@localhost/your_database_name"
```

### Apply Migrations

```
python manage.py migrate
```

### Run the Server

```
python manage.py runserver
```

## Usage

Currently, data is fetched by searching for a YouTube channel name or channel ID.

Plans are in progress to implement full database storage and user-specific features.

## API Integration

We use the YouTube Data API v3 to fetch video information from YouTube channels.

## Steps to Obtain YouTube API Key:

Go to the [Google Cloud Console](https://console.cloud.google.com/).

Create a new project.

Navigate to **APIs & Services > Credentials**.

Click **Create Credentials** > API Key.

Enable the YouTube Data API v3 for your project.

Add the API key to your env.py file.

## Deployment

This project is deployed on Heroku [Live site link](https://ljreach-61418f22471b.herokuapp.com/).

Environment variables for the YouTube API and database are set using Heroku's config vars.

### Deployment Steps:

Log in to Heroku:

```
heroku login
```

Create a new Heroku app:

```
heroku create
```

Push the app to Heroku:

```
git push heroku main
```

Set environment variables in Heroku:

```
heroku config:set YOUTUBE_API_KEY=your_youtube_api_key

heroku config:set DATABASE_URL=your_database_url
```

## Future Plans

Add a front-end form for users to input their YouTube channel ID and retrieve data.

Store channel IDs in a database to allow multiple users to fetch and track their data over time.

Implement more advanced features to display video performance metrics such as watch time, audience engagement, etc.

## Contributing

Feel free to fork this project and submit pull requests. Suggestions and improvements are welcome!

## SECURITY CONCERNS

Note that the YouTube API Key was inadvertently pushed to GitHub in an early commit. The key has been deleted and replaced immediately.

## INTENTIONS

This app is intended for personal research for users to check their own YouTube channel statistics. It is not intended for mass data scraping or commercial purposes.
