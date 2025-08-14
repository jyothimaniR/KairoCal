/**
 * Node test to POST a well-formed JSON payload to voice create-event
 */

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

async function main() {
  const payload = {
    voice_text: 'Schedule a test meeting today at 6 PM',
    user_id: '18209d0d-62c7-48a6-8b49-7fb4e5d3f28e',
    auto_schedule: true,
  };

  console.log('POST', `${API_BASE_URL}/api/v1/voice/create-event`);
  console.log('Payload:', payload);

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/voice/create-event`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const text = await res.text();
    console.log('Status:', res.status);
    try {
      console.log('Body:', JSON.parse(text));
    } catch {
      console.log('Body (raw):', text);
    }
  } catch (err) {
    console.error('Request failed:', err?.message || err);
  }
}

// Ensure fetch exists (Node 18+). If not, instruct to upgrade Node.
if (typeof fetch !== 'function') {
  console.error('Global fetch is not available. Please run with Node.js v18+');
  process.exit(1);
}

main();
