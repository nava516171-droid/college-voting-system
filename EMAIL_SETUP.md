# Email Configuration Guide - OTP Sending Setup

## Overview
The College Voting System now supports sending OTP codes directly to user email addresses using Gmail SMTP. This guide will help you configure email sending.

## Prerequisites
- A Gmail account (personal or business)
- 2-Factor Authentication enabled on your Gmail account
- Basic understanding of environment variables

## Step-by-Step Setup

### 1. Enable 2-Factor Authentication (Required for App Passwords)

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Scroll to "How you sign in to Google"
3. Click on "2-Step Verification"
4. Follow the on-screen instructions to enable 2FA
5. You'll need to verify your phone number

### 2. Generate Gmail App Password

1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select **Mail** from the dropdown
3. Select **Windows Computer** (or your platform)
4. Click **Generate**
5. Google will show you a 16-character password
6. **Copy this password** (you'll need it next)

### 3. Configure Environment Variables

1. Create a `.env` file in the project root (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your Gmail credentials:
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx
   SENDER_NAME=College Voting System
   SENDER_EMAIL=your-email@gmail.com
   ```

3. Replace:
   - `your-email@gmail.com` with your actual Gmail address
   - `xxxx xxxx xxxx xxxx` with the 16-character App Password (without spaces in code)

### 4. Test Email Configuration

Run the test script to verify email sending works:

```bash
# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Test OTP email functionality
python -c "
from app.utils.email import send_otp_email
result = send_otp_email('test@example.com', '123456', 'Test User')
print('✅ Email test successful!' if result else '❌ Email test failed!')
"
```

## Usage - OTP Endpoints

### Request OTP
```bash
curl -X POST http://localhost:8000/api/otp/request \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

**Response:**
```json
{
  "message": "OTP sent to your email",
  "email": "user@example.com",
  "expires_in_minutes": 10
}
```

### Verify OTP
```bash
curl -X POST http://localhost:8000/api/otp/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "otp_code": "123456"}'
```

## Troubleshooting

### Error: "SMTP Authentication Failed"
- ✅ Verify 2-Factor Authentication is **enabled**
- ✅ Verify you're using an **App Password** (not regular password)
- ✅ Copy the 16-character password exactly as shown (include spaces in display, remove in code)
- ✅ Check that `SMTP_USER` matches your Gmail address

### Error: "Connection timeout"
- ✅ Verify `SMTP_SERVER=smtp.gmail.com` (not mail.google.com)
- ✅ Verify `SMTP_PORT=587` (not 465)
- ✅ Check your internet connection
- ✅ Verify firewall isn't blocking port 587

### Emails Not Arriving
- ✅ Check spam/junk folder
- ✅ Verify `SENDER_EMAIL` matches your Gmail account
- ✅ Verify recipient email is correct in the request
- ✅ Wait a few seconds (might be delayed)

### Still Having Issues?
1. Check console output for error messages
2. Verify all `.env` values are correct
3. Ensure Gmail account has 2FA enabled
4. Try a different recipient email address
5. Check Gmail account security settings at [myaccount.google.com/security](https://myaccount.google.com/security)

## Security Notes

⚠️ **Important Security Considerations:**
- Never commit `.env` file to version control (it contains credentials)
- Use `.env.example` as template for other developers
- Rotate your App Password periodically
- Use a dedicated email account for production systems
- Consider using environment variables or secrets management in production (AWS Secrets Manager, Azure Key Vault, etc.)

## For Production Deployment

If deploying to production (Heroku, Railway, AWS, etc.):

1. **Set environment variables** in your hosting platform's dashboard
   - Don't include `.env` files in deployment
   - Use platform's native secrets management

2. **Use a dedicated email service** (recommended):
   - SendGrid
   - AWS SES
   - Mailgun
   - Microsoft 365

3. **Update SMTP credentials**:
   - Use service provider's SMTP settings
   - Implement retry logic
   - Add email logging

## Alternative Email Services

### SendGrid (Recommended for production)
```env
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.xxxxxxxxxxxxx
```

### AWS SES
```env
SMTP_SERVER=email-smtp.region.amazonaws.com
SMTP_PORT=587
SMTP_USER=username
SMTP_PASSWORD=password
```

### Mailgun
```env
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@yourdomain.com
SMTP_PASSWORD=password
```

---

**Questions?** Check the main README.md or test the endpoints via [Swagger UI](http://localhost:8000/docs)
