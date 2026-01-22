# Camera Access Troubleshooting Guide

## Quick Test Steps

### Step 1: Check Your Connection
Open this URL on your phone: **http://10.244.110.136:3000**

### Step 2: Navigate to Face Capture
1. Go through the login/OTP process
2. You should reach the "Face Capture" page
3. The page will say "Loading face detection models..."

### Step 3: Check Initial Status Screen
The page should show what camera API support is available on your browser.

**If you see:**
- ✅ "Camera ready. Please blink once to capture your face." → Your camera is working!
- ❌ "Camera API not available" → Your browser doesn't support camera access (see solutions below)
- ❌ "Camera permission denied" → Grant permission (see solutions below)

### Step 4: Use the Debug Page
If camera isn't working, click the **"🔧 Debug Face"** button to get detailed diagnostic information.

---

## Common Issues and Solutions

### Issue 1: "undefined (reading 'getusermedia')" Error
**What it means:** Your browser doesn't expose the camera API (`navigator.mediaDevices` is undefined)

**Solutions (try in order):**
1. **Use Chrome Mobile** (most reliable)
   - Download Chrome from Google Play Store (Android) or App Store (iPhone)
   - Open http://10.244.110.136:3000
   - Grant camera permission when prompted

2. **Use Firefox Mobile**
   - Download Firefox from Google Play Store (Android) or App Store (iPhone)
   - Open http://10.244.110.136:3000
   - Grant camera permission

3. **Check Browser Permissions**
   - Go to Phone Settings → Apps → [Browser Name] → Permissions
   - Enable "Camera"
   - Reload the page

4. **Restart Browser**
   - Close the browser completely
   - Clear cache (Settings → Apps → [Browser] → Storage → Clear Cache)
   - Open http://10.244.110.136:3000 again

5. **Try HTTP vs HTTPS**
   - Currently using: **HTTP** (http://10.244.110.136:3000)
   - If that doesn't work, HTTPS might be required
   - Contact your system administrator for HTTPS setup

---

### Issue 2: "Camera Permission Denied" Error
**What it means:** The browser asked for permission but you denied it

**Solutions:**
1. **Grant Permission Through Settings**
   - Phone Settings → Privacy/Security → Camera
   - Find your browser name
   - Enable camera access
   - Go back to the app and refresh

2. **Grant Permission When Prompted**
   - Go to http://10.244.110.136:3000
   - When browser asks "Allow access to camera?", tap **"Allow"**
   - Do NOT tap "Block" or "Don't allow"

3. **Clear Browser Data and Try Again**
   - Open browser settings
   - Clear browsing data / cache
   - Go to http://10.244.110.136:3000
   - Grant permission

---

### Issue 3: "No Camera Found" Error
**What it means:** Your device has no camera or it's disabled

**Solutions:**
1. **Check if device has camera**
   - Most phones have cameras
   - If yours doesn't, camera access won't work
   - Try a different device

2. **Check if camera is enabled**
   - Phone Settings → Camera
   - Make sure camera is not disabled
   - Try restarting your phone

3. **Close other apps using camera**
   - Close video call apps (WhatsApp, Teams, Zoom)
   - Close camera app
   - Go back to voting system

---

### Issue 4: "Camera Already in Use" Error
**What it means:** Another app is currently using the camera

**Solutions:**
1. **Close apps using camera**
   - Close: Video calls, camera app, video player
   - Force close if needed: Settings → Apps → [App] → Force Stop
   - Try again

2. **Restart your phone**
   - Sometimes camera gets stuck
   - Turning phone off/on fixes it

---

### Issue 5: "Security Error" or HTTPS Required
**What it means:** Your browser requires HTTPS for camera access

**Solutions:**
1. **If HTTPS is available:**
   - Contact your system administrator
   - Ask for HTTPS URL (instead of HTTP)

2. **Use Firefox Mobile** (supports HTTP on same-network)
   - Download Firefox from app store
   - Firefox allows HTTP camera access within same network

3. **Switch to a different device**
   - Try a tablet or different phone
   - Older devices often support HTTP cameras better

---

## Testing Your Setup

### Method 1: Use the Debug Page
1. Open http://10.244.110.136:3000
2. Click **"🔧 Debug Face"** button (visible on login page)
3. Look at the debug info:
   - **Browser Detection:** Shows what browser you're using
   - **Camera API Checks:** Shows if each API is available
   - **Model Loading:** Shows if face-api models loaded
   - **Video Stream:** Shows if camera is actually streaming
   - **Face Detection:** Tests live face detection

### Method 2: Check Browser Console
1. Open http://10.244.110.136:3000
2. Press **F12** or **Ctrl+Shift+I** to open Developer Tools
3. Go to **Console** tab
4. Look for camera-related messages
5. Take a screenshot to send to support

---

## What Information to Provide to Support

If camera still doesn't work, please provide:

1. **Your Phone Model**
   - Example: Samsung Galaxy A12, iPhone 11, etc.

2. **Operating System**
   - Android version or iOS version
   - Example: Android 12, iOS 15

3. **Browser Name and Version**
   - Example: Chrome 120, Firefox 121, Safari

4. **Exact Error Message**
   - Screenshot of error screen
   - What does it say?

5. **Debug Page Information**
   - Go to http://10.244.110.136:3000
   - Click "🔧 Debug Face"
   - Screenshot of debug page
   - Check browser console (F12) for any error messages
   - Screenshot or copy console errors

6. **Network Information**
   - Can you load the page? (http://10.244.110.136:3000)
   - Can you see any content loading?
   - Or does the page not load at all?

---

## Advanced Troubleshooting

### For System Administrators

#### To enable HTTPS:
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes

# Run HTTPS server
set HTTPS=true
set SSL_CRT_FILE=cert.pem
set SSL_KEY_FILE=key.pem
npm start
```

#### Check Backend Connection:
Backend API should be running at: **http://10.244.110.136:8001**

Test with:
```bash
curl http://10.244.110.136:8001/api/health
```

#### Browser Compatibility Matrix:
| Browser | HTTP Support | HTTPS Required | Notes |
|---------|--------------|----------------|-------|
| Chrome  | ❌           | ✅             | Requires HTTPS on Android 10+ |
| Firefox | ✅           | ✅             | Supports HTTP on same-network |
| Safari  | ❌           | ✅             | iOS requires HTTPS |
| Edge    | ❌           | ✅             | Follows Chrome rules |

---

## Quick Reference

**If nothing works, try:**
1. Download Chrome
2. Grant camera permission
3. Reload page
4. Check internet connection
5. Restart phone

**Emergency Contact:**
- Contact: Your System Administrator
- With: Debug page screenshot + exact error message
