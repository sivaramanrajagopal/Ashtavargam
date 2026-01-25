# Railway Deployment Guide for Agent App

## Prerequisites

1. Railway account (https://railway.app)
2. Supabase project set up (see `setup_supabase.md`)
3. OpenAI API key
4. BAV/SAV API and Dasha/Gochara API deployed (or local URLs)

## Step 1: Create Railway Project

1. Go to Railway dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo" (recommended) or "Empty Project"

## Step 2: Configure Environment Variables

In Railway project settings, add these environment variables:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
OPENAI_API_KEY=your-openai-api-key
BAV_SAV_API_URL=https://your-bav-sav-api.railway.app
DASHA_GOCHARA_API_URL=https://your-dasha-gochara-api.railway.app
PORT=8080
```

## Step 3: Configure Build Settings

1. In Railway project, go to Settings
2. Set **Root Directory** (if needed): `/`
3. Set **Build Command**: `pip install -r requirements_agent.txt`
4. Set **Start Command**: `uvicorn agent_app.main:app --host 0.0.0.0 --port $PORT`

Or use the `Procfile.agent`:
- Railway will automatically detect `Procfile.agent` if present
- Or manually set the start command

## Step 4: Deploy

1. Connect your GitHub repository
2. Railway will automatically deploy on push
3. Or manually trigger deployment

## Step 5: Verify Deployment

1. Check Railway logs for any errors
2. Visit your Railway URL (e.g., `https://your-app.railway.app`)
3. Test the `/health` endpoint
4. Test the `/api/agent/query` endpoint

## Step 6: Populate Knowledge Base

After deployment, run the knowledge base population script:

```bash
# SSH into Railway instance or run locally with production Supabase credentials
python agent_app/knowledge/populate_knowledge_base.py
```

Or create a one-time deployment script that runs on first deploy.

## Troubleshooting

### Import Errors
- Ensure all dependencies are in `requirements_agent.txt`
- Check that Python version is compatible (3.9+)

### Environment Variables
- Verify all required variables are set in Railway
- Check for typos in variable names
- Ensure Supabase and OpenAI keys are valid

### API Connection Issues
- Verify BAV/SAV and Dasha/Gochara API URLs are correct
- Check if APIs are accessible from Railway
- Test API endpoints directly

### Supabase Connection
- Verify Supabase URL and key
- Check if pgvector extension is enabled
- Ensure `vedic_knowledge` table exists

## Production Checklist

- [ ] All environment variables set
- [ ] Knowledge base populated
- [ ] API endpoints tested
- [ ] CORS configured (if needed)
- [ ] Logging configured
- [ ] Error handling in place
- [ ] Health check endpoint working
- [ ] Frontend accessible

## Custom Domain (Optional)

1. In Railway project, go to Settings → Domains
2. Add custom domain
3. Configure DNS records as instructed

## Monitoring

- Check Railway logs regularly
- Monitor API response times
- Track OpenAI API usage
- Monitor Supabase usage
