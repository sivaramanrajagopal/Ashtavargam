# Railway PORT Variable Fix

## Problem
Railway was showing error:
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

This happens because `$PORT` is not being expanded in the start command.

## Solution

### Option 1: Use Python Module (Recommended)
Updated `railway.toml` to use:
```toml
startCommand = "python -m uvicorn agent_app.main:app --host 0.0.0.0 --port ${PORT:-8080}"
```

The `${PORT:-8080}` syntax:
- Uses `$PORT` if set by Railway
- Falls back to `8080` if not set
- Works in Railway's environment

### Option 2: Use Railway UI Override
If the above doesn't work, set the start command directly in Railway UI:

1. Go to Railway Dashboard
2. Select your service
3. **Settings** → **Deploy** → **Custom Start Command**
4. Enter:
   ```
   python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080
   ```
   (Railway will automatically set PORT, so you can use a fixed port or use `${PORT}`)

### Option 3: Use Shell Expansion
If Railway supports shell expansion:
```toml
startCommand = "sh -c 'uvicorn agent_app.main:app --host 0.0.0.0 --port ${PORT:-8080}'"
```

## How Railway Sets PORT

Railway automatically sets the `PORT` environment variable. However, in `railway.toml`, you need to use `${PORT}` syntax (not `$PORT`) for proper expansion.

## Verification

After updating, Railway should:
1. Read PORT from environment (set automatically)
2. Expand `${PORT:-8080}` to the actual port number
3. Start uvicorn with the correct port

## Alternative: Hardcode Port

If PORT expansion continues to fail, you can hardcode:
```toml
startCommand = "python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080"
```

Railway will still route traffic correctly even with a hardcoded port.

