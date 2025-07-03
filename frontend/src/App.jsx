import { useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

import { Authenticator } from '@aws-amplify/ui-react';

function App() {
  const [count, setCount] = useState(0);

  return (
    <Authenticator>
      {({ signOut, user }) => (
        <main>
          <h2>Welcome, {user?.username} 👋</h2>
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
