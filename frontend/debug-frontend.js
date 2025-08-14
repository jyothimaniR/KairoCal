/**
 * Frontend Debug Analysis Script
 * Test each component individually to identify issues
 */

const API_BASE = 'http://127.0.0.1:8000';
const API_V1 = `${API_BASE}/api/v1`;

class FrontendDebugger {
  constructor() {
    this.results = {
      api_connectivity: {},
      component_errors: [],
      data_loading: {},
      ui_elements: {}
    };
  }

  async testAPIConnectivity() {
    console.log('🧪 Testing API Connectivity...');
    
    const endpoints = [
      { name: 'Health Check', url: `${API_BASE}/health`, method: 'GET' },
      { name: 'Events List', url: `${API_V1}/events?cognito_sub=test-user-1`, method: 'GET' },
      { name: 'Analytics Health', url: `${API_V1}/analytics/health`, method: 'GET' },
      { name: 'Voice Health', url: `${API_V1}/voice/health`, method: 'GET' },
      { name: 'BERT Classification', url: `${API_V1}/nlp/classify-priority`, method: 'POST', data: { text: 'urgent meeting tomorrow' }},
      { name: 'Priority Trends', url: `${API_V1}/analytics/priority/trends?cognito_sub=test-user-1`, method: 'GET' },
      { name: 'BERT Performance', url: `${API_V1}/analytics/bert/performance?cognito_sub=test-user-1`, method: 'GET' }
    ];

    for (const endpoint of endpoints) {
      try {
        const startTime = Date.now();
        let response;
        
        if (endpoint.method === 'POST') {
          response = await fetch(endpoint.url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(endpoint.data || {})
          });
        } else {
          response = await fetch(endpoint.url);
        }
        
        const duration = Date.now() - startTime;
        const data = response.ok ? await response.json() : null;
        
        this.results.api_connectivity[endpoint.name] = {
          status: response.ok ? '✅ SUCCESS' : '❌ FAILED',
          status_code: response.status,
          duration: `${duration}ms`,
          data_size: data ? JSON.stringify(data).length : 0,
          has_data: !!data
        };
        
        console.log(`${response.ok ? '✅' : '❌'} ${endpoint.name}: ${response.status} (${duration}ms)`);
        
      } catch (error) {
        this.results.api_connectivity[endpoint.name] = {
          status: '🔴 ERROR',
          error: error.message
        };
        console.log(`🔴 ${endpoint.name}: ${error.message}`);
      }
    }
  }

  testUIElements() {
    console.log('🎨 Testing UI Elements...');
    
    const elements = [
      '.voice-command-center',
      '.mini-calendar',
      '.analytics-panel',
      '.conflict-detection',
      '.productivity-overview',
      '.priority-alerts',
      '.todays-schedule',
      '.ai-suggestions'
    ];
    
    elements.forEach(selector => {
      const element = document.querySelector(selector);
      this.results.ui_elements[selector] = {
        exists: !!element,
        visible: element ? !element.hidden && element.offsetParent !== null : false,
        hasContent: element ? element.textContent.trim().length > 0 : false
      };
    });
  }

  checkConsoleErrors() {
    console.log('🐛 Checking Console Errors...');
    
    // Store original console methods
    const originalError = console.error;
    const originalWarn = console.warn;
    
    const errors = [];
    const warnings = [];
    
    console.error = (...args) => {
      errors.push(args.join(' '));
      originalError.apply(console, args);
    };
    
    console.warn = (...args) => {
      warnings.push(args.join(' '));
      originalWarn.apply(console, args);
    };
    
    setTimeout(() => {
      console.error = originalError;
      console.warn = originalWarn;
      
      this.results.component_errors = {
        errors,
        warnings,
        error_count: errors.length,
        warning_count: warnings.length
      };
    }, 5000);
  }

  async runComprehensiveAnalysis() {
    console.log('🔍 KAIROCAL FRONTEND COMPREHENSIVE ANALYSIS');
    console.log('=' .repeat(50));
    
    // Test API connectivity first
    await this.testAPIConnectivity();
    
    // Test UI elements
    this.testUIElements();
    
    // Monitor console errors
    this.checkConsoleErrors();
    
    // Wait for error collection
    setTimeout(() => {
      this.generateReport();
    }, 6000);
  }

  generateReport() {
    console.log('\n📊 FRONTEND ANALYSIS REPORT');
    console.log('=' .repeat(50));
    
    // API Connectivity Report
    console.log('\n🌐 API CONNECTIVITY:');
    Object.entries(this.results.api_connectivity).forEach(([name, result]) => {
      console.log(`  ${result.status} ${name}: ${result.status_code || result.error}`);
    });
    
    // UI Elements Report  
    console.log('\n🎨 UI ELEMENTS:');
    Object.entries(this.results.ui_elements).forEach(([selector, result]) => {
      const status = result.exists ? (result.visible ? '✅ VISIBLE' : '⚠️ HIDDEN') : '❌ MISSING';
      console.log(`  ${status} ${selector}`);
    });
    
    // Error Report
    console.log('\n🐛 CONSOLE ERRORS:');
    console.log(`  Errors: ${this.results.component_errors.error_count || 0}`);
    console.log(`  Warnings: ${this.results.component_errors.warning_count || 0}`);
    
    if (this.results.component_errors.errors?.length) {
      console.log('\n❌ Critical Errors:');
      this.results.component_errors.errors.slice(0, 5).forEach(error => {
        console.log(`    ${error}`);
      });
    }
    
    // Summary
    const apiSuccessRate = Object.values(this.results.api_connectivity)
      .filter(r => r.status.includes('SUCCESS')).length / 
      Object.keys(this.results.api_connectivity).length * 100;
      
    const uiSuccessRate = Object.values(this.results.ui_elements)
      .filter(r => r.exists && r.visible).length / 
      Object.keys(this.results.ui_elements).length * 100;
      
    console.log('\n📈 SUMMARY:');
    console.log(`  API Success Rate: ${apiSuccessRate.toFixed(1)}%`);
    console.log(`  UI Element Success Rate: ${uiSuccessRate.toFixed(1)}%`);
    console.log(`  Overall Health: ${(apiSuccessRate + uiSuccessRate) / 2 > 75 ? '🟢 GOOD' : '🟡 NEEDS ATTENTION'}`);
    
    // Recommendations
    console.log('\n💡 RECOMMENDATIONS:');
    if (apiSuccessRate < 80) {
      console.log('  - Check backend server connectivity');
      console.log('  - Verify API endpoint configurations');
    }
    if (uiSuccessRate < 80) {
      console.log('  - Check component imports and dependencies');
      console.log('  - Verify CSS and styling issues');
    }
    if (this.results.component_errors.error_count > 5) {
      console.log('  - Address critical JavaScript errors first');
      console.log('  - Check browser developer console for details');
    }
  }
}

// Auto-run analysis when script loads
if (typeof window !== 'undefined') {
  const frontendDebugger = new FrontendDebugger();
  frontendDebugger.runComprehensiveAnalysis();
  
  // Make it available globally for manual testing
  window.KairoCalDebugger = frontendDebugger;
}

console.log('🛠️ Frontend Debug Script Loaded');
console.log('Run `KairoCalDebugger.runComprehensiveAnalysis()` to test manually');
