# Face Verification Voting - Quick Test Guide

## Setup
- Both backend and frontend servers are running
- Backend: http://0.0.0.0:8001
- Frontend: http://localhost:3000

## How to Test

### Step 1: Register or Login
1. Open http://localhost:3000
2. Register a new user OR login with existing credentials
3. During registration/first login, you'll be asked to capture your face
4. Position your face clearly and blink once to register it

### Step 2: Navigate to Voting
1. Click on "🗳️ Cast Your Vote" button on the home page
2. The voting page will load showing all candidates

### Step 3: Cast Vote with Face Verification
1. **Select a Candidate**: Click on any candidate card to select them
2. **Click Submit Vote**: The "Submit Vote" button becomes enabled
3. **Face Verification Modal Appears**: A modal overlay with camera access
4. **Position Your Face**: Make sure your face is clearly visible in the camera
5. **Blink Once**: The system will detect your blink and capture your face
6. **Wait for Verification**: The system verifies your face against your registered face
   - If match: "✓ Face verified successfully!" → Vote is cast
   - If no match: Error message displayed, you can try again

### Step 4: See Results
After successful vote, you'll be redirected to the results page

## What's Happening Behind the Scenes

### Frontend Flow:
1. User clicks "Submit Vote"
2. Face verification modal opens
3. face-api.js detects face and eye blinks in real-time
4. When user blinks once, face image is captured
5. Base64-encoded image sent to backend
6. Backend response processed
7. If verified: vote endpoint called with face verification confirmation
8. Results page displayed

### Backend Flow:
1. `/api/face/verify-for-voting` endpoint receives face image
2. Face encoding extracted from image
3. Compared with user's registered face encoding
4. If match (within confidence threshold): verification successful
5. Vote can proceed to be cast

## Test Scenarios

### ✓ Successful Scenario:
- User registered face previously
- Same person captured during voting
- Face matches registration
- **Expected**: Vote cast successfully

### ✗ Failure Scenarios:

#### Scenario 1: Face Not Registered
- User never registered face
- **Expected**: Error: "You need to register your face first"

#### Scenario 2: Different Person
- Different person's face captured
- Face doesn't match registration
- **Expected**: Error: "Your face does not match the registered face"

#### Scenario 3: No Face Detected
- Camera shows blank/no face
- **Expected**: Error: "No face detected. Please position your face clearly."

#### Scenario 4: Camera Permission Denied
- User denies camera access
- **Expected**: Error message about camera permissions

## Visual Indicators

### Camera Feed:
- **Green Box**: Face detection bounding box (when face detected)
- **Green Dots**: Face landmarks (eyes, nose, mouth, etc.)
- **Text Display**: "Blinks: 0/1" → counts blinks detected

### Status Messages:
- 📍 "Loading face detection models..."
- 📍 "Requesting camera access..."
- 📍 "Camera ready. Position your face and blink once to verify."
- ✓ "Face captured! Uploading..."
- ✓ "Verifying your face..."
- ✓ "Face verified successfully!"
- ✗ Various error messages

## Troubleshooting

### "Camera not supported" message:
- Use Chrome, Firefox, or Safari (latest versions)
- Some older browsers may not support camera APIs

### "Permission Denied" error:
1. Check browser permissions for camera access
2. Allow camera access when prompted
3. Refresh the page
4. Try again

### "Face not detected" error:
- Ensure good lighting in the room
- Position face fully in camera view
- Avoid backlight (light behind you)
- Keep face at normal distance from camera

### "Face does not match" error:
- Ensure it's the same person who registered
- Try to match the angle/distance from registration
- Clean camera lens
- Improve lighting if needed

## Notes

- Face verification is **required** before every vote
- Each user can only vote once per election (enforced by backend)
- Face data is securely compared using advanced face recognition
- No personal face data is stored in plain form (encoded format only)
- The system matches faces for voter authentication purposes only
