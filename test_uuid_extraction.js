// Test UUID extraction fix
const testAlertId = "alert-40f9d17a-8d03-4b13-9363-ead5dee9e5da";
const testUUID = "40f9d17a-8d03-4b13-9363-ead5dee9e5da";

console.log("Test Alert ID:", testAlertId);
console.log("Expected UUID:", testUUID);

// Old broken method
const brokenExtraction = testAlertId.split('-')[1];
console.log("❌ Broken extraction (split('-')[1]):", brokenExtraction);
console.log("❌ Broken length:", brokenExtraction.length);

// New fixed method
const fixedExtraction = testAlertId.substring(6);
console.log("✅ Fixed extraction (substring(6)):", fixedExtraction);
console.log("✅ Fixed length:", fixedExtraction.length);
console.log("✅ Matches expected?", fixedExtraction === testUUID);
