# 📧 OTP Email Sending - Quick Start Guide

## What's New?
Your College Voting System now sends OTP codes directly to user email addresses using Gmail SMTP.

## Quick Setup (5 minutes)

### 1️⃣ Gmail Configuration
```
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to: https://myaccount.google.com/apppasswords
4. Select Mail + Windows Computer
5. Copy the 16-character password
```

### 2️⃣ Create .env File
```bash
cp .env.example .env
```

Edit `.env` and add:
```env
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
```

### 3️⃣ Test Email Configuration
```bash
# Activate venv
.\venv\Scripts\Activate.ps1

# Test email setup
python test_email.py
```

### 4️⃣ Start Server
```bash
python main.py
```

## Using OTP Email API

### Request OTP
```bash
curl -X POST http://localhost:8000/api/otp/request \
  -H "Content-Type: application/json" \
  -d '{"email": "user@college.edu"}'
```

**User receives OTP in their email inbox** ✅

### Verify OTP
```bash
curl -X POST http://localhost:8000/api/otp/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "user@college.edu", "otp_code": "123456"}'
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/otp/request` | POST | Send OTP to email |
| `/api/otp/verify` | POST | Verify OTP code |
| `/api/otp/status` | GET | Check OTP status |
| `/api/otp/resend` | POST | Resend OTP to email |

## Test via Swagger UI
1. Open: http://localhost:8000/docs
2. Navigate to "OTP" section
3. Click "Try it out" on `/api/otp/request`
4. Check your email for the OTP code

## Email Template Features
✅ Professional HTML email design  
✅ Clear OTP code display  
✅ Expiration time (10 minutes)  
✅ Security notices  
✅ Responsive design  

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Auth failed" | Check SMTP_PASSWORD - use App Password, not regular password |
| "Connection timeout" | Verify SMTP_SERVER=smtp.gmail.com and SMTP_PORT=587 |
| No email received | Check spam folder, verify recipient email in request |
| 2FA not enabled | Go to Google Account Security and enable it first |

## Production Deployment

For production, use dedicated email service:
- **SendGrid** (recommended)
- **AWS SES**
- **Mailgun**

See `EMAIL_SETUP.md` for detailed configuration.

## Security Tips
⚠️ Never commit `.env` to git  
⚠️ Use App Passwords, not regular passwords  
⚠️ Rotate credentials periodically  
⚠️ Use environment variables in production  

---

📖 **Full documentation:** See `EMAIL_SETUP.md`  
🧪 **Test script:** Run `python test_email.py`  
📡 **API docs:** Visit `http://localhost:8000/docs`
