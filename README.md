# YouTube Channel Data Fetcher

This project is designed to retrieve video data from a YouTube channel using the YouTube Data API v3.

The data fetched includes video titles, publication dates, view counts, like counts, comment counts, and more.

This app is currently under development, with plans to allow users to input their own channel IDs, store data in a database, and provide a basic front-end interface.

## Features

Fetches data for YouTube videos from a given channel.

Stores video information (e.g., video ID, title, view count) in a PostgreSQL database.

Plans for a basic front-end interface where users can input their channel IDs and fetch video data.

Data is retrieved using the YouTube Data API and is stored securely, with API keys handled via environment variables.

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

Currently, data is fetched using a predefined YouTube channel ID. You can update this in the code for now.

Plans are in progress to implement a front-end where users can input their own YouTube channel IDs.

## API Integration

We use the YouTube Data API v3 to fetch video information from YouTube channels.

## Steps to Obtain YouTube API Key:

Go to the Google Cloud Console.

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

Store channel IDs in the database to allow multiple users to fetch data for their own channels.

Implement more features to display data, like video performance metrics, in the front-end.

## Contributing

Feel free to fork this project and submit pull requests. Suggestions and improvements are welcome!

## SECURITY CONCERNS

Inadvertently sent API_KEY to github on initial commit, deleted and replaced key immediately.

## INTENTIONS

This app is intended for personal research for users to check their own
channel statistics.
