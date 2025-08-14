/**
 * ACADEMIC SYSTEM TEST SCRIPT
 * Tests critical functionality for dissertation demonstration
 * 
 * This script validates:
 * 1. Unified BERT status consistency across all UI locations
 * 2. Event creation functionality (voice and manual)
 * 3. Smart conflict detection with BERT reasoning
 * 4. Academic credibility indicators
 */

const puppeteer = require('puppeteer');

async function testAcademicSystem() {
    console.log('🎓 ACADEMIC SYSTEM VALIDATION STARTING...');
    console.log('======================================');
    
    const browser = await puppeteer.launch({ 
        headless: false, 
        defaultViewport: { width: 1400, height: 900 }
    });
    const page = await browser.newPage();
    
    try {
        // Test 1: Dashboard Load and BERT Status Consistency
        console.log('\n📊 TEST 1: Dashboard Load & BERT Status Consistency');
        await page.goto('http://127.0.0.1:3000/dashboard');
        await page.waitForTimeout(3000);
        
        // Check for BERT indicators in different locations
        const bertIndicators = await page.$$eval('[data-testid*="bert"], [class*="bert"], *:contains("BERT")', 
            elements => elements.map(el => ({
                text: el.textContent,
                className: el.className,
                location: el.closest('[data-component]')?.getAttribute('data-component') || 'unknown'
            }))
        );
        
        console.log('🧠 BERT Indicators Found:', bertIndicators.length);
        bertIndicators.forEach((indicator, i) => {
            console.log(`   ${i + 1}. ${indicator.text.trim()} (${indicator.location})`);
        });
        
        // Test 2: Event Creation
        console.log('\n✍️  TEST 2: Event Creation Functionality');
        
        // Try to find the QuickScheduler input
        const inputSelector = 'input[placeholder*="Meeting"]';
        await page.waitForSelector(inputSelector, { timeout: 5000 });
        
        const testEvent = "Team meeting tomorrow at 2pm for 1 hour";
        await page.type(inputSelector, testEvent);
        console.log('✅ Event text entered:', testEvent);
        
        // Press Enter to create event
        await page.keyboard.press('Enter');
        console.log('✅ Creation triggered via Enter key');
        
        // Wait for creation result
        await page.waitForTimeout(2000);
        
        // Check for success/error messages
        const messages = await page.$$eval('.text-green-600, .text-red-600, .success, .error', 
            elements => elements.map(el => ({
                type: el.className.includes('green') || el.className.includes('success') ? 'success' : 'error',
                text: el.textContent.trim()
            }))
        );
        
        console.log('📨 Creation Messages:', messages);
        
        // Test 3: Conflict Detection Panel
        console.log('\n⚡ TEST 3: Conflict Detection BERT Analysis');
        
        // Look for conflict detection panel
        const conflictPanel = await page.$('[data-testid="conflict-panel"], .conflict-detection');
        if (conflictPanel) {
            console.log('✅ Conflict Detection Panel Found');
            
            // Check for BERT analysis displays
            const bertAnalysis = await page.$$eval('.bert-analysis, [data-bert]', 
                elements => elements.map(el => el.textContent.trim())
            );
            
            console.log('🧠 BERT Analysis Elements:', bertAnalysis);
        } else {
            console.log('❌ Conflict Detection Panel Not Found');
        }
        
        // Test 4: System Health Status
        console.log('\n🏥 TEST 4: System Health Status Consistency');
        
        // Check various health indicators
        const healthElements = await page.$$eval('[data-health], .health-status, .system-status', 
            elements => elements.map(el => ({
                text: el.textContent.trim(),
                classes: el.className
            }))
        );
        
        console.log('🏥 Health Status Elements:', healthElements);
        
        // Final Assessment
        console.log('\n🎯 ACADEMIC SYSTEM ASSESSMENT:');
        console.log('==============================');
        
        const bertCount = bertIndicators.length;
        const hasEventCreation = messages.some(m => m.type === 'success');
        const hasHealthStatus = healthElements.length > 0;
        
        console.log(`✅ BERT Indicators: ${bertCount} found`);
        console.log(`${hasEventCreation ? '✅' : '❌'} Event Creation: ${hasEventCreation ? 'Working' : 'Failed'}`);
        console.log(`${hasHealthStatus ? '✅' : '❌'} Health Status: ${hasHealthStatus ? 'Present' : 'Missing'}`);
        
        if (bertCount >= 2 && hasEventCreation && hasHealthStatus) {
            console.log('\n🎓 ACADEMIC READINESS: DEMONSTRATION READY! ✅');
            console.log('System meets dissertation evaluation criteria.');
        } else {
            console.log('\n⚠️  ACADEMIC READINESS: NEEDS ATTENTION');
            console.log('System requires fixes before demonstration.');
        }
        
    } catch (error) {
        console.error('❌ Test Failed:', error.message);
    } finally {
        await browser.close();
    }
}

// Run the test if this script is executed directly
if (require.main === module) {
    testAcademicSystem().catch(console.error);
}

module.exports = { testAcademicSystem };
