// Quick script to force user data update in the UI
console.log('Clearing old user data...');
localStorage.removeItem('kairocal-user-data');

console.log('Setting new user data...');
const newUserData = {
  full_name: 'Jyothimani',
  email: 'jyothimani1197@gmail.com',
  account_status: 'active'
};

localStorage.setItem('kairocal-user-data', JSON.stringify(newUserData));

console.log('Triggering UI update...');
window.dispatchEvent(new CustomEvent('user-updated', { 
  detail: newUserData 
}));

console.log('User data updated successfully!');
console.log('New user data:', newUserData);
