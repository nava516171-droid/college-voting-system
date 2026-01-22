# Phone Camera Testing Checklist

## Before Testing

- [ ] Phone is charged (at least 50%)
- [ ] Phone is connected to same network as desktop
- [ ] Network: **Same WiFi or Local Network**
- [ ] Desktop is running backend: `python main.py` on 0.0.0.0:8001
- [ ] Desktop is running frontend: `serve -s build -l tcp://0.0.0.0:3000`
- [ ] Camera app works on your phone (basic test)
- [ ] Other apps can access camera

---

## Test URL

```
http://10.244.110.136:3000
```

**Note:** If different IP address, replace 10.244.110.136 with actual server IP.

---

## Testing Sequence

### Step 1: Load Website
- [ ] Open Chrome/Firefox on phone
- [ ] Go to http://10.244.110.136:3000
- [ ] Page loads (you see login screen)
- [ ] Time to load: ______ seconds

### Step 2: Login
- [ ] Enter test email: `test@test.com`
- [ ] Click "Send OTP"
- [ ] You see OTP input screen

### Step 3: Enter OTP
- [ ] Check backend console for OTP (should be printed)
- [ ] OTP: ________
- [ ] Enter OTP in phone
- [ ] Click "Verify OTP"

### Step 4: Face Capture Page Loads
- [ ] You see "Loading face detection models..."
- [ ] Page doesn't crash
- [ ] Status updates to next step

### Step 5: Models Load
- **Status messages in order:**
  - [ ] "Loading tinyFaceDetector..."
  - [ ] "Loading face landmarks..."
  - [ ] "Loading face expressions..."
  - [ ] "Requesting camera access..."

### Step 6: Camera Permission Prompt
- **What you should see:**
  - [ ] Browser asks "Allow access to camera?" (or similar)
  - [ ] Two buttons: "Allow" and "Don't Allow"
  
- **What you should do:**
  - [ ] Tap **"Allow"** (not "Don't Allow")

### Step 7: Camera Access Result
- **Check what happens:**
  - [ ] Camera stream appears (video preview)
  - [ ] You can see yourself in the camera
  - [ ] Status says "Camera ready. Please blink once..."
  
  **OR**
  
  - [ ] Red error message appears
  - [ ] Error text is: ____________________

### Step 8: If Camera Works - Blink Detection
- [ ] Position face in camera view
- [ ] Look at camera
- [ ] Blink once
- [ ] System detects blink (you see "Blink detected")
- [ ] Face is captured
- [ ] You proceed to next page

---

## Error Scenarios

### If Error: "Camera API not available"
- [ ] Check browser type (Chrome? Firefox? Safari? Other?)
- [ ] Check phone OS (Android? iOS?)
- [ ] Try: Close browser → Clear cache → Reload
- [ ] Try: Use Chrome or Firefox instead
- [ ] Try: Restart phone

### If Error: "Camera permission denied"
- [ ] When page asked "Allow camera?", did you tap "Allow"?
- [ ] If not, go to phone Settings → Apps → [Browser] → Permissions → Camera → Enable
- [ ] Reload page

### If Error: "No camera found"
- [ ] Does your phone have a camera? (most do)
- [ ] Try: Restart phone
- [ ] Try: Close other camera apps (camera app, video call apps)

### If Error: "Camera already in use"
- [ ] Close camera app
- [ ] Close video call apps
- [ ] Close video streaming apps
- [ ] Close any other apps using camera

### If Error: "Security error" or "HTTPS required"
- [ ] Some phones require HTTPS
- [ ] Try: Use Firefox (more lenient)
- [ ] Try: Different phone or tablet
- [ ] Contact: System administrator for HTTPS setup

### If Error: "browser doesn't support"
- [ ] Try: Download Chrome or Firefox
- [ ] Try: Update your browser to latest version
- [ ] Try: Use a different device

---

## Data to Collect (If Error Occurs)

**Take screenshots of:**
1. [ ] Error message on phone
2. [ ] Status messages before error
3. [ ] Browser address bar (to confirm URL)

**Open browser console (F12):**
1. [ ] Go to Console tab
2. [ ] Look for red error messages
3. [ ] Screenshot all errors
4. [ ] Search for "Camera" related messages

**Collect information:**
- Phone model: _______________________
- OS version: _________________________
- Browser name & version: _____________
- Error message (exact text): __________
- Console errors: ______________________

---

## Success Criteria

✅ **Test PASSED if:**
- Page loads successfully
- Models load without errors
- Camera permission prompt appears
- User taps "Allow"
- Camera stream appears on screen
- User can see themselves in video
- Blink is detected
- Face is captured
- Proceeds to voting page

❌ **Test FAILED if:**
- Any error message appears
- Camera doesn't start
- Video stream doesn't show
- Blink not detected after 30 seconds

---

## Next Steps After Camera Works

### Step 9: Candidate Selection
- [ ] Page shows candidates
- [ ] You can select one candidate
- [ ] Selection is confirmed

### Step 10: Vote Submission
- [ ] You can confirm vote
- [ ] Vote is submitted
- [ ] Confirmation page appears

### Step 11: Logout
- [ ] You can logout
- [ ] Redirected to login page
- [ ] System works for new user

---

## Multiple Device Testing

Test with different phone models:

| Device | OS | Browser | Status | Notes |
|--------|----|---------|----|-------|
| ______ | __ | ______ | [ ] ✅ [ ] ❌ | |
| ______ | __ | ______ | [ ] ✅ [ ] ❌ | |
| ______ | __ | ______ | [ ] ✅ [ ] ❌ | |

---

## Debugging Steps (If Stuck)

### Use Debug Page
1. Open: http://10.244.110.136:3000
2. Click: "🔧 Debug Face" button
3. Look at: Browser detection, Camera API checks
4. Note: Any red X's or failures
5. Screenshot everything

### Check Backend Logs
1. Look at terminal running Python backend
2. Search for: "Camera", "OTP", "Error"
3. Note: Any error messages
4. Send: Screenshot of backend terminal

### Check Browser Console
1. Press: F12 (Developer Tools)
2. Go to: Console tab
3. Reload: The page
4. Look for: Red errors
5. Screenshot: All error messages

---

## Quick Debug Commands (For Developers)

```javascript
// In browser console (F12 → Console tab):

// Check camera API availability
navigator.mediaDevices
navigator.mediaDevices.getUserMedia
navigator.getUserMedia

// Check if page is HTTPS or HTTP
console.log(window.location.protocol)

// Check face-api loaded
console.log(faceapi)

// Check for model loading issues
faceapi.nets.tinyFaceDetector.isLoaded
```

---

## Support Information

**If you need help:**
1. Take all screenshots from above
2. Note exact error message
3. Provide device info (model, OS, browser)
4. Run debug page and screenshot
5. Contact: Your System Administrator

**Send:**
- Error screenshots
- Debug page screenshot
- Browser console screenshot
- Device info
- Exact error message
