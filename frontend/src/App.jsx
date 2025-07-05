import { useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

const formFields = {
  signUp: {
    email: {
      label: 'Email',
      placeholder: 'Enter your email',
      required: true,
    },
    given_name: {
      label: 'First Name',
      placeholder: 'Enter your first name',
      required: true,
    },
    password: {
      label: 'Password',
      placeholder: 'Enter your password',
      required: true,
    },
    confirm_password: {
      label: 'Confirm Password',
      placeholder: 'Confirm your password',
      required: true,
    },
  },
};

function App() {
  const [count, setCount] = useState(0);

  return (
    <Authenticator formFields={formFields}>
      {({ signOut, user }) => (
        <main>
          <h2>Welcome, {user?.attributes?.given_name} 👋</h2>
          <button onClick={signOut}>Sign out</button>

          <div>
            <a href="https://vite.dev" target="_blank" rel="noreferrer">
              <img src={viteLogo} className="logo" alt="Vite logo" />
            </a>
            <a href="https://react.dev" target="_blank" rel="noreferrer">
              <img src={reactLogo} className="logo react" alt="React logo" />
            </a>
            <h1>Vite + React</h1>
            <div className="card">
              <button onClick={() => setCount((count) => count + 1)}>
                count is {count}
              </button>
              <p>
                Edit <code>src/App.jsx</code> and save to test HMR
              </p>
            </div>
            <p className="read-the-docs">
              Click on the Vite and React logos to learn more
            </p>
          </div>
        </main>
      )}
    </Authenticator>
  );
}

export default App;
