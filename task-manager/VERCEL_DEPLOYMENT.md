# Vercel Deployment Guide

This guide will help you deploy your Task Manager application to Vercel.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Git repository (GitHub, GitLab, or Bitbucket)
3. Your code pushed to the repository

## Important Notes

### ⚠️ SQLite Database Limitation

**SQLite does NOT work well on serverless platforms like Vercel** because:
- Serverless functions are stateless
- Each function invocation may run on a different server
- File system writes are temporary and lost between invocations

**Recommended Solutions:**
1. **Use a cloud database** (recommended):
   - **Vercel Postgres** (free tier available)
   - **Supabase** (free tier available)
   - **PlanetScale** (free tier available)
   - **MongoDB Atlas** (free tier available)

2. **Use Vercel KV** (Redis) for simple key-value storage

3. **Use an external API** for data persistence

## Deployment Steps

### Step 1: Push to Git Repository

Make sure your code is pushed to GitHub, GitLab, or Bitbucket.

### Step 2: Connect to Vercel

1. Go to https://vercel.com
2. Click "Add New Project"
3. Import your Git repository
4. Select the repository containing your Task Manager project

### Step 3: Configure Build Settings

Vercel should auto-detect the settings, but verify:

- **Framework Preset**: Other
- **Root Directory**: `task-manager` (or leave blank if root)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/build`
- **Install Command**: `cd frontend && npm install`

### Step 4: Set Environment Variables

In Vercel project settings, add these environment variables:

```
REACT_APP_API_URL=https://your-app-name.vercel.app/api
ALLOWED_ORIGINS=https://your-app-name.vercel.app,http://localhost:3000
DB_FILE=/tmp/task_manager.db
```

**Note**: Replace `your-app-name` with your actual Vercel app name.

### Step 5: Deploy

Click "Deploy" and wait for the build to complete.

## Post-Deployment

### Update CORS Origins

After deployment, update the `ALLOWED_ORIGINS` environment variable in Vercel to include your actual domain:

```
ALLOWED_ORIGINS=https://your-actual-domain.vercel.app,http://localhost:3000
```

### Test Your Deployment

1. Visit your Vercel URL
2. Check the browser console for any errors
3. Test creating, reading, updating, and deleting tasks

## Troubleshooting

### "Failed to fetch" Error

- Check that the backend API is accessible at `/api/health`
- Verify CORS settings include your Vercel domain
- Check browser console for specific error messages

### Database Not Working

- SQLite won't persist data on serverless
- Switch to a cloud database (see recommendations above)
- Update `main.py` to use the new database connection

### Build Fails

- Check build logs in Vercel dashboard
- Ensure all dependencies are in `package.json` and `requirements.txt`
- Verify Python version compatibility (Vercel uses Python 3.9)

## File Structure for Vercel

```
task-manager/
├── api/
│   └── index.py          # Vercel serverless function handler
├── backend/
│   ├── main.py           # FastAPI application
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json      # Node dependencies
├── vercel.json           # Vercel configuration
├── .vercelignore         # Files to ignore
└── .env.example          # Environment variable template
```

## Next Steps

1. **Set up a cloud database** (highly recommended)
2. **Update database connection** in `backend/main.py`
3. **Test thoroughly** before sharing with users
4. **Set up custom domain** (optional)

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Review browser console errors
3. Verify environment variables are set correctly
4. Test API endpoints directly: `https://your-app.vercel.app/api/health`

