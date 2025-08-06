# Firebase Setup Instructions for KairoCal

## 🚀 Quick Setup Steps

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project"
3. Name your project: `kairocal` (or your preferred name)
4. Enable Google Analytics (optional)
5. Click "Create project"

### 2. Add Web App
1. In your Firebase project dashboard, click the "Web" icon (`</>`)
2. Register app name: `KairoCal Frontend`
3. **Important**: Check "Also set up Firebase Hosting" if you want to deploy later
4. Click "Register app"
5. Copy the configuration object that appears

### 3. Update Configuration
Replace the placeholder config in `src/lib/firebase.ts` with your actual config:

```javascript
const firebaseConfig = {
  apiKey: "your-actual-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id", 
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "your-actual-app-id"
};
```

### 4. Enable Authentication
1. In Firebase Console, go to "Authentication" > "Get started"
2. Go to "Sign-in method" tab
3. Enable these providers:
   - **Email/Password**: Click to enable
   - **Google**: 
     - Click to enable
     - Add your support email
     - Add authorized domains if needed

### 5. Configure Authorized Domains (Important!)
1. In Authentication > Settings > Authorized domains
2. Add these domains:
   - `localhost` (for development)
   - Your production domain when ready

### 6. Test Your Setup
1. Save your firebase.ts file with the real config
2. Start your dev server: `npm run dev`
3. Try signing up with email or Google!

## 🔧 Optional: Firestore Database
If you want to store user data:
1. Go to "Firestore Database" > "Create database"
2. Choose "Start in test mode" for now
3. Select a region close to your users

## 📱 Environment Variables (Recommended)
For production, store your config in environment variables:

Create `.env.local`:
```
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=your-app-id
```

Then update `firebase.ts` to use them:
```javascript
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};
```

## ✅ What You Get
- ✅ Email/Password authentication
- ✅ Google OAuth sign-in
- ✅ Password reset functionality
- ✅ Protected routes
- ✅ User session management
- ✅ Beautiful custom UI (no Cognito limitations!)
- ✅ Real-time auth state updates

Ready to test! 🎉
