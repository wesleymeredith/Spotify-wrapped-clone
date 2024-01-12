Spotify Wrapped Clone
===
A Flask-based web application that replicates the Spotify Wrapped experience, showcasing users' top artists and tracks.

## Overview

This project aims to provide a user-friendly interface for displaying Spotify Wrapped data. Users can log in securely via Spotify, and the application retrieves and presents their top artists and tracks in an organized and visually appealing manner.

## Features

- **Dynamic Web Application:**
  - Implemented a dynamic Flask-based web application for a user-friendly Spotify Wrapped interface.

- **Spotify API Integration:**
  - Integrated Spotify API using Spotipy to retrieve user-specific top artists and tracks data.

- **Secure User Authentication:**
  - Developed OAuth2 authentication for secure user login and access token handling.

- **User Authentication System:**
  - Established a user authentication system, allowing secure access to top artists' data.

- **Visually Appealing Webpage:**
  - Designed and implemented a dynamic webpage to present the user's top artists in an organized and visually appealing manner.

## Getting Started

### Prerequisites

- Python installed
- Spotify Developer Account

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/spotify-wrapped-clone.git
   cd spotify-wrapped-clone
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set-up your Spotify developer crendentials:
   - Create a Spotify Developer account [here](https://developer.spotify.com/).
Create a new app to obtain your CLIENT_ID and CLIENT_SECRET.
Set the redirect URI to http://127.0.0.1:5000/redirectPage.
Create a .env file and add your credentials
4. Run the application
```bash
flask --app main run
```
Visit the local host IP in the browser.

### Contributing
Contributions are welcome! If you have ideas for improvements, open an issue or create a pull request.
