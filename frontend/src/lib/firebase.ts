// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAKYDZkLpiIEiGNseujZP78RkPQ_2GAdDM",
  authDomain: "kairocal2025.firebaseapp.com",
  projectId: "kairocal2025",
  storageBucket: "kairocal2025.firebasestorage.app",
  messagingSenderId: "677367683104",
  appId: "1:677367683104:web:25e5ec307c970a3e664445",
  measurementId: "G-ZNCPM46N6D"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);

// Initialize Cloud Firestore and get a reference to the service
export const db = getFirestore(app);

export default app;