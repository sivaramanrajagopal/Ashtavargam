# Railway Deployment Fix - SQLite Library Issue

## Problem
`pyswisseph` requires system libraries (libsqlite3.so.0) that aren't available in Railway's default Python buildpack.

## Solution
Created `Dockerfile` that installs required system dependencies.

## Files Created

1. **`Dockerfile`** - Main deployment configuration
   - Installs SQLite development libraries
   - Installs build tools needed for pyswisseph
   - Sets up Python environment

2. **`railway.toml`** - Railway-specific configuration
   - Specifies Dockerfile as builder
   - Sets health check and restart policies

3. **`.railwayignore`** - Files to exclude from deployment
   - Reduces deployment size
   - Excludes test files and documentation

## Deployment Steps

### Option 1: Railway Auto-Detection
Railway should automatically detect the `Dockerfile` and use it.

1. Push code to GitHub
2. Railway detects `Dockerfile`
3. Builds using Docker
4. Deploys automatically

### Option 2: Manual Configuration
If auto-detection doesn't work:

1. Go to Railway Dashboard
2. Select your service
3. Settings → Build
4. Set "Build Command" to use Dockerfile
5. Or set "Builder" to "Dockerfile"

## Verification

After deployment, check logs to ensure:
- ✅ No `ImportError: libsqlite3.so.0` errors
- ✅ Flask app starts successfully
- ✅ Health check responds

## If Issues Persist

1. **Check Railway logs:**
   - View build logs to see if Dockerfile is being used
   - Check runtime logs for any errors

2. **Verify Dockerfile is detected:**
   - Railway should show "Building with Dockerfile" in build logs

3. **Test locally:**
   ```bash
   docker build -t ashtakavarga-test .
   docker run -p 5004:5004 ashtakavarga-test
   ```

## Alternative: Buildpack with aptfile

If Docker doesn't work, create `aptfile`:
```
libsqlite3-dev
build-essential
libc6-dev
```

But Dockerfile approach is preferred for better control.

