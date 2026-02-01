# Phase 1 Testing Guide

## ✅ Phase 1 Changes Summary

### 1. XSS Protection
- ✅ Added DOMPurify library (CDN)
- ✅ Created `escapeHtml()` function
- ✅ Created `sanitizeHtml()` function  
- ✅ Updated `formatMessage()` to escape HTML
- ✅ Sanitized message rendering with DOMPurify

### 2. CORS Configuration
- ✅ Replaced `allow_origins=["*"]` with specific origins
- ✅ Set `allow_credentials=False`
- ✅ Limited methods to `GET, POST, OPTIONS`
- ✅ Limited headers to needed ones only
- ✅ Added `ALLOWED_ORIGINS` environment variable support

### 3. Input Validation
- ✅ Added `max_length=1000` to `QueryRequest.query`
- ✅ Added validator to check query length
- ✅ Added query sanitization

---

## 🧪 Testing Checklist

### Test 1: Basic Functionality
- [ ] Start agent app: `cd agent_app && python -m uvicorn main:app --port 8080`
- [ ] Open browser: `http://localhost:8080/chat`
- [ ] Enter birth details and start chat
- [ ] Send a test message
- [ ] Verify message displays correctly
- [ ] Check browser console for errors

### Test 2: XSS Protection
- [ ] Try sending: `<script>alert('XSS')</script>`
- [ ] Try sending: `<img src=x onerror="alert('XSS')">`
- [ ] Try sending: `**Bold** and *italic* text`
- [ ] Verify:
  - Scripts don't execute
  - HTML is escaped/sanitized
  - Markdown formatting still works

### Test 3: CORS Configuration
- [ ] Check browser DevTools → Network tab
- [ ] Look for CORS headers in responses
- [ ] Verify API calls work from frontend
- [ ] Check for CORS errors in console

### Test 4: Input Validation
- [ ] Try sending a query with 1001 characters
- [ ] Verify error message appears
- [ ] Try sending empty query
- [ ] Verify validation works

### Test 5: Mobile Interface
- [ ] Test on mobile device (or browser DevTools mobile mode)
- [ ] Verify chat interface works
- [ ] Test all modals (Ashtakavarga, Dasha, etc.)
- [ ] Check for layout issues

---

## 🐛 Common Issues & Fixes

### Issue 1: DOMPurify not loading
**Symptom:** Console error: `DOMPurify is not defined`

**Fix:** Check internet connection (CDN requires internet). For offline, download DOMPurify locally.

### Issue 2: CORS errors
**Symptom:** `Access-Control-Allow-Origin` errors

**Fix:** 
1. Check `ALLOWED_ORIGINS` environment variable
2. Ensure your origin is in the list
3. For localhost: `ALLOWED_ORIGINS=http://localhost:8080`

### Issue 3: Messages not displaying
**Symptom:** Messages appear blank or with HTML tags

**Fix:** Check if `formatMessage()` is working correctly. Verify DOMPurify is loaded.

---

## ✅ Success Criteria

Phase 1 is successful if:
- ✅ All basic functionality works
- ✅ XSS attacks are blocked (scripts don't execute)
- ✅ CORS is configured correctly (no CORS errors)
- ✅ Input validation works (long queries rejected)
- ✅ No console errors
- ✅ Mobile interface works

---

## 📝 Next Steps After Testing

### If Tests Pass:
```bash
# Commit Phase 1
git add agent_app/
git commit -m "feat(security): Phase 1 - Fix XSS and CORS vulnerabilities"

# Proceed to Phase 2
```

### If Tests Fail:
1. Note the specific issue
2. Check browser console for errors
3. Review the changes in `agent_app/`
4. Fix issues and re-test

---

## 🔄 Rollback Plan

If Phase 1 causes issues:
```bash
# Go back to main branch
git checkout main

# Or revert specific files
git checkout main -- agent_app/main.py agent_app/templates/chat.html
```

---

## 📊 Testing Results Template

```
Date: ___________
Tester: ___________

Test 1: Basic Functionality
[ ] Pass [ ] Fail
Notes: _______________________

Test 2: XSS Protection
[ ] Pass [ ] Fail
Notes: _______________________

Test 3: CORS Configuration
[ ] Pass [ ] Fail
Notes: _______________________

Test 4: Input Validation
[ ] Pass [ ] Fail
Notes: _______________________

Test 5: Mobile Interface
[ ] Pass [ ] Fail
Notes: _______________________

Overall: [ ] Ready for Phase 2 [ ] Needs fixes
```

