# Karaoke Flask Web App

The Karaoke Flask Web App is a fun, interactive application allowing users to search for karaoke songs, start sessions, and invite friends to join. This application integrates with the YouTube API to fetch karaoke videos, enhancing the karaoke experience.

## Features

- Song search via YouTube API
- Session management for group karaoke experiences (TODO)
- Queue system for song lineup (TODO)
- User-friendly interface for seamless interaction (TODO)
- User accounts for tracking song and session history (TODO)
- Lists for managing favorite songs (TODO)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or later
- Flask
- Docker (for containerization)
- Google Cloud account (for deployment)

### Setting Up for Development

1. **Fork and Clone the repository**

After forking the repo, you can clone it to your local machine.


2. **Configure Environment Variables**

Before running the application, ensure that all necessary environment variables are set. These include database connection settings, application secret keys, and other necessary configurations. These should be set in a .env file at the root of the project directory.

```
YOUTUBE_API_KEY=youtube_api_key

MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=your_database_name
MYSQL_USER=your_user_name
MYSQL_PASSWORD=your_password
DATABASE_HOST=db

```


3. **Start the Application**

With Docker and Docker Compose installed, and the environment variables configured, you can start the application by running the following command from the root of the project directory:

```
docker-compose up -d
```
This command builds and starts the containers in detached mode. Your application container and MySQL database container will be started.

4. **Accessing the Application**
After the containers are up and running, you can access the Flask application by running the following command from the root of the project directory:

```
docker-compose exec web flask run
```

Then navigate to `http://127.0.0.1:5000` in your web browser (assuming port 5000 is exposed in your docker-compose.yml).



### Deployed version on Google Cloud

The current version (V1.0.0) can currently be accessed at [https://karaoke-app-goaslfxq3a-uk.a.run.app/](https://karaoke-app-goaslfxq3a-uk.a.run.app/)


## Acknowledgments

- YouTube Data API for providing song search capabilities
- Flask community for the extensive documentation and resources
- Google Cloud Run for the seamless deployment experience