# Mobile Access Setup Guide

## Problem
When clicking the login link from email on a mobile phone, the page opens but shows "server not fetched" error.

## Cause
The email link was pointing to `localhost:3000` which doesn't work on mobile phones. The frontend needs to be accessible from the mobile device's network.

## Solution

### Step 1: Find Your Machine's IP Address
Run this command on your Windows machine:
```powershell
ipconfig
```

Look for the IPv4 address under your active network adapter (usually in the `192.168.x.x` or `10.x.x.x` range).

Example: `192.168.1.100`

### Step 2: Update Backend Configuration
Edit the `.env` file in the root directory:

```bash
# Change this:
FRONTEND_URL=http://localhost:3000

# To your machine IP (replace 192.168.1.100 with your actual IP):
FRONTEND_URL=http://192.168.1.100:3000
```

### Step 3: Restart the Backend Server
Kill the running backend process and restart it:
```bash
python main.py
```

### Step 4: Access from Mobile Phone
Make sure your phone and computer are on the same network.

1. **For Desktop**: Visit `http://localhost:3000`
2. **For Mobile**: Visit `http://192.168.1.100:3000` (replace with your actual IP)

### Step 5: Email Links
- New email links sent after updating the configuration will contain the correct URL
- Example: `http://192.168.1.100:3000/login?token=xyz123`

## How It Works Now

1. **Backend** sends email links using the `FRONTEND_URL` environment variable
2. **Frontend** (when accessed via mobile IP) automatically uses the same IP to connect to the backend
3. **Mobile phone** can now access both the frontend and call the backend API

## Testing the Setup

1. Register from mobile: `http://192.168.1.100:3000`
2. Check email for login link
3. Click login link on mobile - should work now!
4. Click "Forgot Password" to get a new login link with the correct URL

## Troubleshooting

**Still getting "server not fetched"?**
- Check if your phone is on the same WiFi network as your computer
- Verify the IP address is correct by running `ipconfig` again
- Make sure the backend server is running
- Check firewall settings - make sure port 8001 is accessible
- Try accessing `http://192.168.1.100:8001/docs` from your mobile browser

