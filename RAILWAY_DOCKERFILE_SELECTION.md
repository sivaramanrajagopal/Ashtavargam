# Railway Dockerfile Selection Guide

## Which Dockerfile to Use for Each Service

### For BAV/SAV API Service:
**Dockerfile Path:** `Dockerfile`

- This is the **original Dockerfile** in your repo
- It's designed for the Flask app but works for the API too
- **OR** you can leave it **empty** - Railway will auto-detect it

**Settings:**
- Dockerfile Path: `Dockerfile` (or empty)
- Build Command: `pip install -r requirements.txt`
- Start Command: `python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080`

---

### For Dasha/Gochara API Service:
**Dockerfile Path:** **(Leave Empty)**

- This service doesn't need a Dockerfile
- Railway will use the build command directly
- Simpler deployment

**Settings:**
- Dockerfile Path: **(empty - leave blank)**
- Build Command: `pip install -r requirements_agent.txt`
- Start Command: `python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8080`

---

### For Agent App Service:
**Dockerfile Path:** `Dockerfile.agent`

- This is already configured
- Uses the agent-specific Dockerfile
- Don't change this!

**Settings:**
- Dockerfile Path: `Dockerfile.agent` ✅ (already set)
- Start Command: `python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080` ✅ (already set)

---

## Quick Reference

| Service | Dockerfile Path | Build Command | Start Command |
|---------|----------------|---------------|---------------|
| **BAV/SAV API** | `Dockerfile` (or empty) | `pip install -r requirements.txt` | `python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8080` |
| **Dasha/Gochara API** | **(empty)** | `pip install -r requirements_agent.txt` | `python3 -m uvicorn dasha_gochara_api:app --host 0.0.0.0 --port 8080` |
| **Agent App** | `Dockerfile.agent` | (auto) | `python -m uvicorn agent_app.main:app --host 0.0.0.0 --port 8080` |

---

## For Your Current Step (BAV/SAV API):

**In the Railway UI, set:**
- **Dockerfile Path:** `Dockerfile`
  - Type exactly: `Dockerfile` (no leading slash, no path)
  - OR leave it empty - Railway will find it automatically

**Why:**
- The original `Dockerfile` has all the system dependencies needed
- It installs `requirements.txt` which has all API dependencies
- Works perfectly for the BAV/SAV API service

---

## Note

If you leave Dockerfile Path **empty**, Railway will:
1. Look for `Dockerfile` in the root directory
2. Use it automatically if found
3. This is often the simplest option!

**Recommendation:** For BAV/SAV API, you can either:
- Set it to `Dockerfile` explicitly, OR
- Leave it empty (Railway will auto-detect)

Both will work! 🎯

