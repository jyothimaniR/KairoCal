const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  console.log('=== Testing Dashboard Components Directly ===');
  
  // Mock localStorage authentication for development
  await page.goto('http://localhost:5174/auth');
  await page.waitForTimeout(1000);
  
  // Mock a Firebase user session in localStorage/sessionStorage
  await page.evaluate(() => {
    // Mock Firebase auth state
    localStorage.setItem('firebase:authUser:cncih8g9fhdcnirv8q3vjht7g:[DEFAULT]', JSON.stringify({
      uid: 'test-user-123',
      email: 'test@example.com',
      displayName: 'Test User',
      emailVerified: true
    }));
    
    // Mock additional session data if needed
    sessionStorage.setItem('firebase:host:auth.firebase.googleapis.com', 'true');
  });
  
  console.log('✅ Mock authentication data set');
  
  // Now try to access dashboard
  await page.goto('http://localhost:5174/dashboard');
  await page.waitForTimeout(3000); // Wait longer for React to process auth state
  
  const finalUrl = page.url();
  console.log(`Final URL: ${finalUrl}`);
  
  if (finalUrl.includes('/dashboard')) {
    console.log('🎉 Successfully accessed dashboard!');
    await page.screenshot({ path: 'dashboard-direct-screenshot.png', fullPage: true });
    console.log('✅ Dashboard screenshot taken: dashboard-direct-screenshot.png');
  } else {
    console.log('❌ Still redirected to auth page');
    await page.screenshot({ path: 'auth-redirect-screenshot.png', fullPage: true });
    console.log('📸 Auth redirect screenshot taken: auth-redirect-screenshot.png');
  }
  
  await browser.close();
})();
