# Railway Deployment Guide

## Quick Deploy to Railway

1. **Install Railway CLI** (optional but recommended):
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize Railway Project**:
   ```bash
   railway init
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

## Manual Deployment via GitHub

1. **Push code to GitHub repository**

2. **Go to Railway Dashboard** (https://railway.app)

3. **Create New Project** → **Deploy from GitHub repo**

4. **Select your repository**

5. **Railway will automatically detect**:
   - Python runtime
   - `Procfile` for web process
   - `requirements.txt` for dependencies

6. **Set Environment Variables** (if needed):
   - `PORT` - Automatically set by Railway
   - `FLASK_ENV` - Set to `production` for production deployments

## Configuration Files

- **Procfile**: Defines the web process (`web: python app_complete.py`)
- **requirements.txt**: Python dependencies including Flask, pyswisseph, gunicorn
- **app_complete.py**: Main application (automatically reads `PORT` from environment)

## Verification

After deployment, Railway will provide a public URL. Test the app:
- Home page: `/`
- Results page: `/ashtakavarga-prokerala`

## Mobile & Tablet Support

The app is fully responsive with:
- Mobile-friendly forms and inputs
- Scrollable tables on small screens
- Adaptive grid layouts for BAV charts
- Touch-optimized navigation

## Troubleshooting

- **Build fails**: Check `requirements.txt` - ensure all dependencies are listed
- **App doesn't start**: Check logs in Railway dashboard
- **Port issues**: Railway automatically sets `PORT` environment variable

