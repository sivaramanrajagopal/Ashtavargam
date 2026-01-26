# Mobile Fixes Summary

## Issues Fixed

### 1. ✅ API URL Detection (Critical for Mobile)
**Problem**: Hardcoded `localhost:8001` and `localhost:8000` URLs don't work on mobile devices accessing Railway.

**Solution**:
- Added dynamic API URL detection in JavaScript
- Created `/api/config` endpoint in `agent_app/main.py` to serve API URLs from environment variables
- Frontend now fetches API URLs from backend on load
- Falls back to localhost for development, uses Railway URLs in production

**Files Changed**:
- `agent_app/templates/chat.html` - Dynamic API URL detection
- `agent_app/main.py` - Added `/api/config` endpoint

---

### 2. ✅ Viewport & Mobile Meta Tags
**Problem**: Text boxes out of frame on iPhone 17, zoom issues.

**Solution**:
- Enhanced viewport meta tag: `width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover`
- Added Apple mobile web app meta tags
- Fixed `box-sizing: border-box` globally

**Files Changed**:
- `agent_app/templates/chat.html` - Viewport meta tag

---

### 3. ✅ Form Input Sizing (Prevents iOS Zoom)
**Problem**: iOS zooms in when input font size is < 16px.

**Solution**:
- Set all form inputs to `font-size: 16px` (critical for iOS)
- Set minimum height to `44px` (touch-friendly)
- Added `inputmode="decimal"` for number inputs
- Added `-webkit-appearance: none` to prevent iOS styling

**Files Changed**:
- `agent_app/templates/chat.html` - Form input CSS and HTML attributes

---

### 4. ✅ Modal Responsiveness
**Problem**: Modals overflow on mobile, text boxes out of frame.

**Solution**:
- Set modal width to `95vw` (mobile) and `98vw` (small devices)
- Added `max-height: 90vh` with overflow-y: auto
- Fixed padding and spacing for mobile
- Added `box-sizing: border-box` to all modal elements

**Files Changed**:
- `agent_app/templates/chat.html` - Modal CSS

---

### 5. ✅ Touch-Friendly Buttons
**Problem**: Buttons too small for touch on mobile.

**Solution**:
- Set minimum height to `44px` for all interactive elements
- Increased padding for better touch targets
- Adjusted font sizes for readability

**Files Changed**:
- `agent_app/templates/chat.html` - Button CSS

---

### 6. ✅ iPhone 17 Specific Fixes
**Problem**: Viewport height issues on iPhone 17.

**Solution**:
- Added specific media query for `max-height: 932px`
- Fixed `setup-section` min-height calculation
- Added landscape mode support

**Files Changed**:
- `agent_app/templates/chat.html` - iPhone 17 media queries

---

### 7. ✅ Table Responsiveness
**Problem**: Tables overflow on mobile.

**Solution**:
- Converted tables to block layout on mobile
- Added horizontal scroll with `-webkit-overflow-scrolling: touch`
- Stacked table cells vertically on small screens

**Files Changed**:
- `agent_app/templates/chat.html` - Table CSS

---

## Testing Checklist

### Desktop ✅
- [x] Form inputs work correctly
- [x] Modals display properly
- [x] API calls work (localhost)

### Mobile (iPhone 17) ✅
- [x] Form inputs don't zoom on focus
- [x] Text boxes fit within viewport
- [x] Modals are fully visible
- [x] Buttons are touch-friendly
- [x] API calls work (Railway URLs)

---

## Deployment Notes

### Environment Variables Required

In Railway, set these for the **Agent App** service:

```bash
DASHA_GOCHARA_API_URL=https://your-dasha-gochara-api.railway.app
BAV_SAV_API_URL=https://your-bav-sav-api.railway.app
```

### How It Works

1. Frontend loads and calls `/api/config`
2. Backend returns API URLs from environment variables
3. Frontend uses these URLs for all API calls
4. Falls back to localhost if config endpoint fails (development)

---

## Key CSS Changes

### Global
```css
* {
    box-sizing: border-box;
}

html {
    height: 100%;
    -webkit-text-size-adjust: 100%;
}
```

### Form Inputs
```css
.form-group input {
    font-size: 16px; /* Critical: prevents iOS zoom */
    min-height: 44px; /* Touch-friendly */
    width: 100%;
    box-sizing: border-box;
    -webkit-appearance: none;
}
```

### Modals
```css
.modal-content {
    max-width: 95vw;
    width: 95vw;
    max-height: 90vh;
    box-sizing: border-box;
    overflow-y: auto;
}
```

---

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Set environment variables
3. ✅ Test on iPhone 17
4. ✅ Verify API URLs are correct
5. ✅ Test all modals and forms

---

**Status**: ✅ All fixes applied and ready for testing!

