# SoundPath Full Stack Application

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here

# Session Secret (generate a random string)
SECRET_KEY=your_secret_key_here_make_it_long_and_random_123456789
```

### 2. Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Configure the OAuth consent screen
6. Create a Web application client ID
7. Add these authorized redirect URIs:
   - `http://localhost:8000/auth` (for development)
   - `http://localhost:5173/auth` (alternative)

### 3. Running the Application

```bash
# Build and start all services
docker-compose up --build

# Or start individual services
docker-compose up mongo
docker-compose up backend
docker-compose up frontend
```

### 4. Development Mode

For frontend development without Docker:

```bash
cd frontend
npm install
npm run dev
```

### 5. Troubleshooting

- **OAuth Error**: Make sure Google OAuth credentials are properly configured
- **Docker Build Error**: Ensure all dependencies are compatible (React 18, Node 18)
- **Database Connection**: MongoDB should be running on port 27017

## Features

- Google OAuth Authentication
- User Profile Management
- Equipment Recommendations
- Starter Kits
- Community Features
