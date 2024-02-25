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

1. **Clone the repository**

```
git clone https://github.com/yourusername/karaoke-app.git
cd karaoke-app
```

2. **Create and activate a virtual environment**

```
python3 -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```

3.  **Install required packages**

```
pip install -r requirements.txt
```

4. **Set up environment variables**

Copy the `.env.example` file to a new file named `.env` and fill in the required API keys and other configurations.

5. **Run the Flask application locally**

```
flask run
```

The application will be available at `http://localhost:5000`.

### Dockerization

To containerize the application using Docker, follow these steps:

1. **Build the Docker image**

```
docker build -t karaoke-app:latest .
```

2. **Run the container**

```
docker run -p 5000:5000 karaoke-app:latest
```

The application will now be accessible at `http://localhost:5000`.

### Deployed version on Google Cloud

The current version (V1.0.0) can currently be accessed at [https://karaoke-app-goaslfxq3a-uk.a.run.app/](https://karaoke-app-goaslfxq3a-uk.a.run.app/)


## Acknowledgments

- YouTube Data API for providing song search capabilities
- Flask community for the extensive documentation and resources
- Google Cloud Run for the seamless deployment experience