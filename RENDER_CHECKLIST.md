# Render Deployment Checklist ✅

## Pre-Deployment (Local)
- [ ] Commit all changes to GitHub
- [ ] Test locally: `npm start` (frontend) and `python main.py` (backend)
- [ ] Verify requirements.txt is complete
- [ ] Check .env variables are set
- [ ] Update api.js with correct backend URL

## Render Setup
- [ ] Create Render account at render.com
- [ ] Connect GitHub repository
- [ ] Generate secret key for SECRET_KEY env var

## Database Setup
- [ ] Create PostgreSQL database on Render
- [ ] Copy Internal Database URL
- [ ] Note down credentials

## Backend Deployment
- [ ] Create Web Service for backend
- [ ] Set Environment Variables:
  - [ ] DATABASE_URL (PostgreSQL URL)
  - [ ] SECRET_KEY (generated key)
  - [ ] FRONTEND_URL (leave blank, update after frontend deploys)
  - [ ] SMTP_SERVER (smtp.gmail.com)
  - [ ] SMTP_USER (Gmail address)
  - [ ] SMTP_PASSWORD (Gmail app password)
  - [ ] DEBUG = False
- [ ] Verify backend URL: https://college-voting-backend.onrender.com
- [ ] Check backend health: Open URL + /health

## Frontend Deployment
- [ ] Create Web Service for frontend
- [ ] Set Environment Variables:
  - [ ] REACT_APP_API_URL (backend URL)
- [ ] Verify frontend URL: https://college-voting-frontend.onrender.com
- [ ] Frontend should load successfully

## Post-Deployment
- [ ] Update backend FRONTEND_URL env var with frontend URL
- [ ] Trigger backend redeploy
- [ ] Test user registration
- [ ] Test login with face capture
- [ ] Test OTP verification
- [ ] Test voting functionality
- [ ] Test admin dashboard
- [ ] Verify emails are sending
- [ ] Check mobile access works

## Monitoring
- [ ] Check Render Logs regularly for errors
- [ ] Set up Render alerts (optional paid feature)
- [ ] Monitor database usage

## Optimization (If needed)
- [ ] Upgrade to Hobby Plan for always-on service
- [ ] Increase database plan if hitting limits
- [ ] Enable caching for static files
- [ ] Configure CDN for frontend

---

**Timeline**: 
- Each deployment takes 3-5 minutes
- Total setup time: 15-20 minutes

**Cost**:
- Free tier: $0/month (with limitations)
- Hobby tier: $7/month per service
