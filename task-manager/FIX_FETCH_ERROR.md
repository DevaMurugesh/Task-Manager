# Fix "Failed to fetch" Error on Vercel

## Your Deployment URL
Based on your deployment: `task-manager-ai48.vercel.app`

## Quick Fix Steps

### Step 1: Set Environment Variables in Vercel

Go to your Vercel project dashboard:
1. Click on your project: **task-manager**
2. Go to **Settings** → **Environment Variables**
3. Add these 3 variables:

#### Variable 1:
- **Name:** `REACT_APP_API_URL`
- **Value:** `https://task-manager-ai48.vercel.app/api`
- **Environments:** ✅ Production ✅ Preview ✅ Development

#### Variable 2:
- **Name:** `ALLOWED_ORIGINS`
- **Value:** `https://task-manager-ai48.vercel.app,http://localhost:3000`
- **Environments:** ✅ Production ✅ Preview ✅ Development

#### Variable 3:
- **Name:** `DB_FILE`
- **Value:** `/tmp/task_manager.db`
- **Environments:** ✅ Production ✅ Preview ✅ Development

### Step 2: Redeploy

After adding environment variables:
1. Go to **Deployments** tab
2. Click the **three dots** (⋯) on the latest deployment
3. Click **Redeploy**
4. Wait for deployment to complete

### Step 3: Test the API

Test if your API is working:
1. Visit: `https://task-manager-ai48.vercel.app/api/health`
2. You should see a JSON response like:
   ```json
   {
     "status": "healthy",
     "database": "connected",
     ...
   }
   ```

If the API endpoint works but the frontend still shows "Failed to fetch", continue to Step 4.

### Step 4: Verify Frontend is Using Correct URL

The frontend should automatically use the environment variable. To verify:
1. Open browser console (F12)
2. Check for any CORS errors
3. Check Network tab to see what URL it's trying to fetch

## Common Issues

### Issue 1: Environment Variable Not Set
- **Symptom:** Frontend tries to connect to `http://localhost:8000`
- **Fix:** Make sure `REACT_APP_API_URL` is set in Vercel

### Issue 2: CORS Error
- **Symptom:** Browser console shows CORS error
- **Fix:** Make sure `ALLOWED_ORIGINS` includes your Vercel domain

### Issue 3: API Not Responding
- **Symptom:** `/api/health` returns 404 or error
- **Fix:** Check that `api/index.py` exists and `vercel.json` routes are correct

### Issue 4: Wrong API Path
- **Symptom:** API calls go to wrong URL
- **Fix:** Ensure `REACT_APP_API_URL` ends with `/api` (not `/api/`)

## Testing Checklist

- [ ] Environment variables are set in Vercel
- [ ] Redeployed after setting environment variables
- [ ] `/api/health` endpoint works
- [ ] Browser console shows correct API URL
- [ ] No CORS errors in console
- [ ] Network tab shows successful API calls

## Still Not Working?

If you still get "Failed to fetch":
1. Check Vercel function logs (Deployments → Click deployment → Functions tab)
2. Check browser console for specific error messages
3. Verify the API endpoint: `https://task-manager-ai48.vercel.app/api/tasks`

