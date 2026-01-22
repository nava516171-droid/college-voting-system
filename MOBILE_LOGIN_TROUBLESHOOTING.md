# Mobile Phone Login - Troubleshooting Guide

## Current Setup
- **Backend Server**: Running on `http://10.244.110.136:8001`
- **Frontend Server**: Running on `http://10.244.110.136:3000`
- **Network Connection**: ✅ Verified working

## If You're Still Getting "Failed Fetch" Error on Phone

### Step 1: Verify Network Connection
1. On your phone, make sure you're connected to the **same WiFi network** as your computer
2. Test by pinging from phone: Open terminal/command prompt and type:
   ```
   ping 10.244.110.136
   ```
   Should see replies (low ms values like 1-5ms)

### Step 2: Test Backend Directly
On your phone's browser, try visiting:
```
http://10.244.110.136:8001/docs
```

**Expected Results:**
- Should see Swagger API documentation
- If it shows "Cannot reach server", the issue is network/firewall

### Step 3: Check Firewall
Windows Firewall might be blocking port 8001. To allow it:

**Windows 10/11:**
1. Go to Settings → Privacy & Security → Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Click "Change settings"
4. Click "Allow another app"
5. Click "Browse" → Find `python.exe` in your venv
6. Click "Add" → Make sure both Private and Public are checked

**Or via PowerShell (as Admin):**
```powershell
netsh advfirewall firewall add rule name="College Voting Backend" dir=in action=allow program="C:\Path\To\venv\Scripts\python.exe" enable=yes
netsh advfirewall firewall add rule name="College Voting Backend Port" dir=in action=allow protocol=tcp localport=8001 enable=yes
```

### Step 4: Verify Backend Configuration
Check that `.env` file in root directory has:
```
FRONTEND_URL=http://10.244.110.136:3000
```

If you had to change it, restart the backend:
```
python main.py
```

### Step 5: Check Browser Console on Phone
1. On phone, go to `http://10.244.110.136:3000`
2. Open Developer Console (usually F12 or Ctrl+Shift+I)
3. Look for error messages that show:
   - Exact URL it's trying to reach
   - Network error or timeout
   
### Step 6: Test Connection Helper Page
Visit this page on your phone to diagnose connection issues:
```
http://10.244.110.136:3000/test-connection.html
```

This will run automated tests and show you exactly what's working and what's not.

## Common Issues and Solutions

### "Cannot find the server"
- ❌ Phone is not on same WiFi as computer
- ❌ Wrong IP address
- ❌ Backend is not running
- ✅ Solution: Check WiFi connection, verify IP with `ipconfig`, restart backend

### "Connection timeout"
- ❌ Firewall is blocking the connection
- ❌ Port 8001 is not listening
- ✅ Solution: Allow port through firewall, verify backend is running with `netstat -ano | findstr "8001"`

### "Invalid or expired login link"
- ❌ Token is old (>24 hours)
- ❌ Backend database was reset
- ✅ Solution: Register again to get a new token

### "Login failed"
- ❌ Wrong email/password
- ❌ Backend can't connect to database
- ✅ Solution: Check credentials, check database connection

## Quick Diagnostic Commands

**Check if backend is running:**
```
netstat -ano | findstr "8001"
Should show: TCP    0.0.0.0:8001           0.0.0.0:0              LISTENING
```

**Check if frontend is running:**
```
netstat -ano | findstr "3000"
Should show: TCP    0.0.0.0:3000           0.0.0.0:0              LISTENING
```

**Test backend from computer:**
```
curl http://10.244.110.136:8001/api/elections
Should return JSON array of elections
```

## Emergency Fix: Use localhost on Computer

If firewall is blocking mobile access, you can still test on desktop:

1. From browser on same computer: `http://localhost:3000`
2. Everything should work normally
3. For production/mobile, will need to resolve firewall issue

## Still Not Working?

1. Check Windows Defender logs for blocked connections
2. Try disabling firewall temporarily (not recommended for production)
3. Check if a VPN or proxy is interfering
4. Look at backend terminal for error messages when you try to login
5. Check browser console (F12) for detailed error messages
