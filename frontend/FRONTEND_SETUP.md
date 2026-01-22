# React Frontend Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure API URL
Create a `.env` file in the `frontend` directory:
```
REACT_APP_API_URL=http://localhost:8000
```

### 3. Start the Development Server
```bash
npm start
```

The app will open at `http://localhost:3000`

## Features

✅ **Login Page** - Email & password authentication
✅ **OTP Verification** - Verify OTP sent to email
✅ **Candidate Voting** - Select and vote for candidates
✅ **Live Results** - View real-time election results
✅ **Responsive Design** - Works on desktop and mobile
✅ **Error Handling** - User-friendly error messages

## How It Works

1. **Login** - User enters email and password
2. **OTP Verification** - User enters OTP from email
3. **Select Candidate** - Click on candidate card to select
4. **Cast Vote** - Submit vote to backend
5. **View Results** - See live results with vote counts

## File Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── pages/
│   │   ├── LoginPage.js
│   │   ├── OTPPage.js
│   │   ├── VotingPage.js
│   │   └── ResultsPage.js
│   ├── styles/
│   │   ├── LoginPage.css
│   │   ├── OTPPage.css
│   │   ├── VotingPage.css
│   │   └── ResultsPage.css
│   ├── api.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## API Integration

The frontend connects to your FastAPI backend at:
- **Development**: http://localhost:8000
- **Production**: Your deployed backend URL

All API calls are in `src/api.js`

## Building for Production

```bash
npm run build
```

This creates a production build in the `build` folder.

## Deployment

To deploy the React app:
1. Build: `npm run build`
2. Upload `build` folder to your hosting (Netlify, Vercel, etc.)
3. Configure API URL for production environment

## Customization

- **Colors**: Edit color values in CSS files
- **Candidate Cards**: Modify `VotingPage.js` UI
- **Results Display**: Customize `ResultsPage.js` layout

---

Ready to run? Let me know if you need help!
