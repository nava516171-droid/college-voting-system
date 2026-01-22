# Voting System Deployment Guide

## Quick Start with Railway

### Step 1: Create Railway Account
- Go to [https://railway.app](https://railway.app)
- Sign up with GitHub/Google
- Verify email

### Step 2: Connect Repository
1. Click "New Project" → "Deploy from GitHub"
2. Connect your GitHub account
3. Select the college voting system repository

### Step 3: Configure Environment Variables
In Railway dashboard, add these variables:

```
DATABASE_URL=sqlite:///./voting_system.db
SMTP_USER=thankyounava09@gmail.com
SMTP_PASSWORD=bmkb itio tkma swup
SENDER_EMAIL=thankyounava09@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_NAME=College Voting System
SECRET_KEY=your-secret-key-here
```

**For SECRET_KEY, generate one:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Deploy
- Railway auto-deploys on push to main branch
- Check deployment status in dashboard
- Get your public URL

### Step 5: Test
Your app will be available at: `https://your-app-name.up.railway.app`

Test endpoints:
```
GET  https://your-app-name.up.railway.app/health
GET  https://your-app-name.up.railway.app/docs
POST https://your-app-name.up.railway.app/api/auth/login
```

## Alternative: Render

### Quick Setup
1. Go to [https://render.com](https://render.com)
2. Sign up with GitHub
3. Create "New Web Service"
4. Select your GitHub repo
5. Set Build Command: `pip install -r requirements.txt`
6. Set Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables
8. Deploy

## Production Checklist

- [x] Backend fully tested
- [x] OTP email system working
- [x] Voting endpoints working
- [ ] Custom domain (optional)
- [ ] SSL certificate (automatic on Railway/Render)
- [ ] Database backup setup
- [ ] Monitoring/logging

## Important Notes

1. **Database**: SQLite will work but data resets on redeploy. For production, upgrade to PostgreSQL
2. **Email**: Gmail SMTP configured and tested
3. **Security**: Update SECRET_KEY before deploying
4. **CORS**: Already configured for cross-origin requests

## Database Migration (Optional)

To use PostgreSQL instead of SQLite:

1. Create PostgreSQL database on Railway/Render
2. Get connection string
3. Update `.env`:
```
DATABASE_URL=postgresql://user:password@host:port/dbname
```

4. Rebuild and deploy

## Troubleshooting

**Emails not sending?**
- Check SMTP credentials
- Verify Gmail App Password is correct
- Check deployment logs

**Votes not showing?**
- Check database connection
- Verify API endpoints working with Swagger UI

**Build fails?**
- Check requirements.txt is in root
- Verify Python version matches (3.11)
- Check for syntax errors

---

Ready to deploy? Let me know which platform you choose!
