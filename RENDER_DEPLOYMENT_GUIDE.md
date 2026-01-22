# Render Deployment Guide - College Voting System

## Step 1: Push Your Code to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Prepare for Render deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/college-voting-system.git
git push -u origin main
```

## Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Connect your GitHub repository

## Step 3: Set Up PostgreSQL Database on Render

1. Go to Render Dashboard
2. Click **New +** → **PostgreSQL**
3. Fill in details:
   - **Name**: college-voting-db
   - **Database**: college_voting_system
   - **User**: render_user
   - **Region**: Select closest to you
   - **Plan**: Free (or upgrade if needed)
4. Click **Create Database**
5. **Copy the Internal Database URL** - you'll need this

## Step 4: Deploy Backend

1. Click **New +** → **Web Service**
2. Select your GitHub repository
3. Fill in details:
   - **Name**: college-voting-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python -m alembic upgrade head` (if using migrations)
   - **Start Command**: `gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --timeout 120`
   - **Plan**: Free (or paid)

4. **Set Environment Variables** (scroll down):
   - `DATABASE_URL`: Paste the PostgreSQL URL from step 3
   - `SECRET_KEY`: Generate a random key: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
   - `FRONTEND_URL`: `https://college-voting-frontend.onrender.com` (will be created next)
   - `ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
   - `DEBUG`: `False`
   - `SMTP_SERVER`: `smtp.gmail.com`
   - `SMTP_PORT`: `587`
   - `SMTP_USER`: Your Gmail address
   - `SMTP_PASSWORD`: Your Gmail app password
   - `SENDER_NAME`: `College Voting System`
   - `SENDER_EMAIL`: Your Gmail address

5. Click **Create Web Service**
6. Wait for deployment to complete
7. Copy the service URL (e.g., `https://college-voting-backend.onrender.com`)

## Step 5: Deploy Frontend

1. Click **New +** → **Web Service**
2. Select your GitHub repository again
3. Fill in details:
   - **Name**: college-voting-frontend
   - **Environment**: Node
   - **Build Command**: `cd frontend && npm ci && npm run build`
   - **Start Command**: `cd frontend && npm install -g serve && serve -s build -l 3000`
   - **Plan**: Free (or paid)

4. **Set Environment Variables**:
   - `REACT_APP_API_URL`: Paste backend URL from Step 4 (e.g., `https://college-voting-backend.onrender.com`)

5. Click **Create Web Service**
6. Wait for deployment
7. Access frontend at the provided URL

## Step 6: Update Backend Environment Variable

1. Go back to Backend service
2. Click **Environment** tab
3. Edit `FRONTEND_URL` to point to frontend URL from Step 5
4. Click **Save Changes** - Backend will redeploy

## Step 7: Migrate Database (Important!)

Since Render uses PostgreSQL instead of SQLite:

1. Update your database URL from SQLite to PostgreSQL
2. Run migrations (if you have them):
   ```bash
   python -m alembic upgrade head
   ```

3. Or create tables manually by running in backend:
   ```bash
   python init_database.py
   ```

## Step 8: Test Your Deployment

1. Open your frontend URL
2. Register a new account
3. Log in
4. Try voting
5. Check admin panel

## Troubleshooting

### Deployment Fails
- Check **Logs** tab in Render dashboard
- Common issues:
  - Missing environment variables
  - Database URL incorrect
  - Port binding issues

### Connection Issues
- Verify `FRONTEND_URL` points to correct frontend URL
- Verify `REACT_APP_API_URL` points to correct backend URL
- Check CORS is enabled in backend

### Database Issues
- Ensure PostgreSQL service is running
- Check DATABASE_URL format is correct
- Run migrations if needed

### Email Not Working
- Verify Gmail credentials
- Check app password is correct (not regular password)
- Verify 2FA is enabled on Gmail

## Free Tier Limitations

- Auto-spins down after 15 mins of inactivity
- Limited compute resources
- 400 hours/month total

## Upgrade Options

- **Hobby Plan**: $7/month - Always on, more resources
- **Standard Plan**: $12/month - Production-ready

## Useful Render Commands

### View Logs
- Go to service → **Logs** tab

### Redeploy
- Go to service → Click **Manual Deploy** → **Deploy latest commit**

### Update Environment Variables
- Go to service → **Environment** tab → Edit and save

---

## Next Steps

1. Commit render.yaml: `git add render.yaml && git commit -m "Add Render config"`
2. Push to GitHub: `git push`
3. Create services in Render dashboard
4. Test all features
5. Share your deployed URL!

---

**Your app will be live at**: 
- Frontend: `https://college-voting-frontend.onrender.com`
- Backend API: `https://college-voting-backend.onrender.com`
