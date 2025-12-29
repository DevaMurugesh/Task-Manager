# 🚀 How to Deploy to Vercel - Step by Step

## Prerequisites Checklist

- [ ] Your code is in a Git repository (GitHub, GitLab, or Bitbucket)
- [ ] You have a Vercel account (sign up at https://vercel.com - it's free!)
- [ ] All changes are committed and pushed to your repository

## Step-by-Step Deployment Guide

### Step 1: Prepare Your Code

Make sure all your files are committed and pushed to Git:

```bash
# Check status
git status

# Add all files
git add .

# Commit changes
git commit -m "Ready for Vercel deployment"

# Push to your repository
git push origin main
```

### Step 2: Sign Up / Log In to Vercel

1. Go to **https://vercel.com**
2. Click **"Sign Up"** (or **"Log In"** if you already have an account)
3. Sign up with GitHub, GitLab, or Bitbucket (recommended) or use email

### Step 3: Create New Project

1. Once logged in, click **"Add New..."** button (top right)
2. Click **"Project"**
3. You'll see a list of your repositories

### Step 4: Import Your Repository

1. Find your **Task Manager** repository in the list
2. Click **"Import"** next to your repository
3. If you don't see it, click **"Adjust GitHub App Permissions"** to grant access

### Step 5: Configure Project Settings

Vercel should auto-detect most settings, but verify:

**Project Name:**
- Keep default or change to something like `task-manager`

**Framework Preset:**
- Select **"Other"** or **"Create React App"**

**Root Directory:**
- If your `vercel.json` is in the `task-manager` folder, set: `task-manager`
- If `vercel.json` is in root, leave blank

**Build and Output Settings:**
- **Build Command:** `cd frontend && npm install && npm run build`
- **Output Directory:** `frontend/build`
- **Install Command:** `cd frontend && npm install`

### Step 6: Set Environment Variables ⚠️ IMPORTANT

Before deploying, click **"Environment Variables"** and add:

#### Variable 1:
- **Name:** `REACT_APP_API_URL`
- **Value:** `https://your-app-name.vercel.app/api`
  - ⚠️ Replace `your-app-name` with your actual project name
  - Or leave as placeholder and update after first deployment

#### Variable 2:
- **Name:** `ALLOWED_ORIGINS`
- **Value:** `https://your-app-name.vercel.app,http://localhost:3000`
  - ⚠️ Replace `your-app-name` with your actual project name
  - You can update this after deployment with the real URL

#### Variable 3:
- **Name:** `DB_FILE`
- **Value:** `/tmp/task_manager.db`

**Select environments:** Check all three:
- ✅ Production
- ✅ Preview
- ✅ Development

### Step 7: Deploy!

1. Click **"Deploy"** button
2. Wait for the build to complete (usually 2-5 minutes)
3. You'll see build logs in real-time

### Step 8: After First Deployment

Once deployed, you'll get a URL like: `https://task-manager-abc123.vercel.app`

1. **Update Environment Variables:**
   - Go to **Project Settings** → **Environment Variables**
   - Update `REACT_APP_API_URL` to: `https://your-actual-url.vercel.app/api`
   - Update `ALLOWED_ORIGINS` to: `https://your-actual-url.vercel.app,http://localhost:3000`
   - Click **"Redeploy"** to apply changes

2. **Test Your Deployment:**
   - Visit your Vercel URL
   - Test API: `https://your-url.vercel.app/api/health`
   - Try creating a task
   - Check browser console (F12) for errors

## Quick Deploy via Vercel CLI (Alternative Method)

If you prefer command line:

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy (from project root)
cd task-manager
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No (first time)
# - Project name? task-manager
# - Directory? ./
# - Override settings? No

# Set environment variables
vercel env add REACT_APP_API_URL
vercel env add ALLOWED_ORIGINS
vercel env add DB_FILE

# Deploy to production
vercel --prod
```

## Troubleshooting

### Build Fails

**Error: "Build command failed"**
- Check build logs in Vercel dashboard
- Ensure `package.json` has correct build script
- Verify Node.js version (Vercel uses Node 18+)

**Error: "Python dependencies not found"**
- Ensure `requirements.txt` is in `backend/` folder
- Check that `mangum` is in requirements.txt

### API Not Working

**Error: "Failed to fetch"**
- Check that environment variables are set correctly
- Verify API URL includes `/api` prefix
- Test API endpoint directly: `https://your-app.vercel.app/api/health`
- Check CORS settings in `backend/main.py`

**Error: "Database connection failed"**
- ⚠️ SQLite won't persist on Vercel (serverless limitation)
- Consider switching to a cloud database (see VERCEL_DEPLOYMENT.md)

### Frontend Not Loading

**Blank page or 404**
- Check that `outputDirectory` is set to `frontend/build`
- Verify build completed successfully
- Check browser console for errors

## What Happens After Deployment?

✅ **Automatic Deployments:**
- Every push to `main` branch = Production deployment
- Every push to other branches = Preview deployment
- Pull requests = Preview deployment with unique URL

✅ **Free Features:**
- HTTPS automatically enabled
- Global CDN
- Custom domains (free tier)
- Automatic SSL certificates

## Next Steps

1. **Set up a custom domain** (optional):
   - Go to Project Settings → Domains
   - Add your custom domain

2. **Set up a cloud database** (recommended):
   - SQLite won't persist data on Vercel
   - Use Vercel Postgres, Supabase, or MongoDB Atlas

3. **Monitor your app:**
   - Check Vercel dashboard for analytics
   - Monitor function logs for errors

## Need Help?

- 📖 Full guide: See `VERCEL_DEPLOYMENT.md`
- 🔧 Vercel Docs: https://vercel.com/docs
- 💬 Vercel Support: https://vercel.com/support

