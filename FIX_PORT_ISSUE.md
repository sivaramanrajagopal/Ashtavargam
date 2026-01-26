# Fix $PORT Environment Variable Issue

## Problem
Railway start command is failing with:
```
Error: Invalid value for '--port': '$PORT' is not a valid integer.
```

This happens because `$PORT` is not being expanded as an environment variable in the start command.

## Solution

### Option 1: Use Fixed Port (Recommended)

Railway automatically maps the `PORT` environment variable to your service, so you can use a fixed port in the start command.

**In Railway Dashboard → Settings → Deploy:**

Change the **Start Command** from:
```
python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port $PORT
```

To:
```
python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8080
```

**Why this works**: Railway sets the `PORT` environment variable automatically, but when you use `$PORT` in the start command, it's not expanded. Using a fixed port (8080) works because Railway handles the port mapping internally.

### Option 2: Use Python to Read PORT

Alternatively, you can modify the start command to use Python's `os.environ`:

**Start Command:**
```
python3 -c "import os; import uvicorn; from dasha_gochara_api import app; port = int(os.environ.get('PORT', 8080)); uvicorn.run(app, host='0.0.0.0', port=port)"
```

But Option 1 is simpler and recommended.

## Quick Fix Steps

1. **Go to Railway Dashboard**
2. **Select "Dasha Gochara API" service**
3. **Go to Settings → Deploy section**
4. **Find "Start Command" field**
5. **Change it to:**
   ```
   python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8080
   ```
6. **Save the changes**
7. **Go to Deployments tab**
8. **Click "Redeploy"**
9. **Wait for deployment to complete**

## Verification

After redeployment, check the logs:

1. Go to **Logs** tab
2. Should see:
   ```
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8080
   ```
3. No more `$PORT` errors

## Why This Happens

Railway's start command is executed directly, not through a shell, so environment variable expansion (`$PORT`) doesn't work. Railway sets the `PORT` environment variable, but you need to either:
- Use a fixed port (simplest)
- Use a shell script that expands the variable
- Use Python code to read the environment variable

## For All Services

Apply the same fix to **BAV/SAV API** if it has the same issue:

**Start Command:**
```
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080
```

---

**Note**: The code in `dasha_gochara_api.py` already handles PORT correctly in the `if __name__ == "__main__"` block, but Railway uses the start command from Settings, not the Python file's main block.

