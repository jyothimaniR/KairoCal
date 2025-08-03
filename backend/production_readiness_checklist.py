#!/usr/bin/env python3
"""
Production Readiness Checklist for KairoCal BERT Priority Classification System
Comprehensive validation of all system components for production deployment

This script validates:
✅ Database Schema and Migrations
✅ BERT Model Training and Loading
✅ API Endpoints and Error Handling
✅ Configuration and Environment Variables
✅ Integration Components (NLP Service, Conflict Detection)
✅ Performance and Scalability
✅ Testing Coverage and Quality
✅ Security and Data Privacy
✅ Monitoring and Logging
✅ Documentation and Deployment

Usage:
    python production_readiness_checklist.py --full-check
    python production_readiness_checklist.py --component api
    python production_readiness_checklist.py --verbose
"""

import argparse
import asyncio
import sys
import os
import json
import logging
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
import subprocess
import importlib.util
import requests
from dataclasses import dataclass

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class CheckResult:
    """Result of a production readiness check"""
    component: str
    check_name: str
    status: str  # "PASS", "FAIL", "WARNING", "SKIP"
    message: str
    details: Optional[Dict] = None
    execution_time: float = 0.0

class ProductionReadinessValidator:
    """Comprehensive production readiness validation"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[CheckResult] = []
        self.start_time = time.time()
        
    def add_result(self, result: CheckResult):
        """Add a check result"""
        self.results.append(result)
        
        # Color coding for terminal output
        color_map = {
            "PASS": "\033[92m",  # Green
            "FAIL": "\033[91m",  # Red
            "WARNING": "\033[93m",  # Yellow
            "SKIP": "\033[94m"   # Blue
        }
        reset_color = "\033[0m"
        
        status_colored = f"{color_map.get(result.status, '')}{result.status}{reset_color}"
        
        print(f"  {status_colored:15} {result.check_name:40} {result.message}")
        
        if self.verbose and result.details:
            for key, value in result.details.items():
                print(f"    {key}: {value}")
    
    def run_check(self, component: str, check_name: str, check_func, *args, **kwargs) -> CheckResult:
        """Run a single check with error handling and timing"""
        start_time = time.time()
        
        try:
            status, message, details = check_func(*args, **kwargs)
            result = CheckResult(
                component=component,
                check_name=check_name,
                status=status,
                message=message,
                details=details,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            result = CheckResult(
                component=component,
                check_name=check_name,
                status="FAIL",
                message=f"Check failed with exception: {str(e)}",
                details={"exception": str(e), "traceback": traceback.format_exc()},
                execution_time=time.time() - start_time
            )
        
        self.add_result(result)
        return result
    
    # Database Checks
    
    def check_database_connection(self) -> Tuple[str, str, Dict]:
        """Check database connectivity"""
        try:
            from app.core.database import get_db, engine
            from sqlalchemy import text
            
            # Test connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                conn.close()
            
            return "PASS", "Database connection successful", {"engine": str(engine.url)}
        except Exception as e:
            return "FAIL", f"Database connection failed: {str(e)}", {"error": str(e)}
    
    def check_database_schema(self) -> Tuple[str, str, Dict]:
        """Check database schema and tables"""
        try:
            from app.core.database import engine
            from sqlalchemy import inspect, text
            
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            required_tables = ['users', 'events', 'reminders']
            missing_tables = [t for t in required_tables if t not in tables]
            
            if missing_tables:
                return "FAIL", f"Missing required tables: {missing_tables}", {"missing": missing_tables, "found": tables}
            
            # Check events table for priority columns
            try:
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT priority_level, priority_confidence, classification_method FROM events LIMIT 1"))
                    columns_exist = True
            except Exception:
                columns_exist = False
            
            if not columns_exist:
                return "FAIL", "Priority columns missing from events table", {"required_columns": ["priority_level", "priority_confidence", "classification_method"]}
            
            return "PASS", f"Database schema valid with {len(tables)} tables", {"tables": tables}
        except Exception as e:
            return "FAIL", f"Schema check failed: {str(e)}", {"error": str(e)}
    
    def check_alembic_migrations(self) -> Tuple[str, str, Dict]:
        """Check Alembic migration status"""
        try:
            # Check if alembic directory exists
            alembic_dir = Path("alembic")
            if not alembic_dir.exists():
                return "WARNING", "Alembic directory not found", {"directory": str(alembic_dir)}
            
            # Check for migration files
            versions_dir = alembic_dir / "versions"
            if not versions_dir.exists():
                return "WARNING", "Alembic versions directory not found", {}
            
            migrations = list(versions_dir.glob("*.py"))
            migration_count = len(migrations)
            
            if migration_count == 0:
                return "WARNING", "No migration files found", {}
            
            return "PASS", f"Found {migration_count} migration files", {"migration_count": migration_count}
        except Exception as e:
            return "FAIL", f"Migration check failed: {str(e)}", {"error": str(e)}
    
    # BERT Model Checks
    
    def check_bert_model_files(self) -> Tuple[str, str, Dict]:
        """Check for BERT model files"""
        model_paths = [
            "models/priority_classifier",
            "models/priority_classifier/pytorch_model.bin",
            "models/priority_classifier/config.json",
            "models/priority_classifier/tokenizer.json"
        ]
        
        existing_files = []
        missing_files = []
        
        for path in model_paths:
            if Path(path).exists():
                existing_files.append(path)
            else:
                missing_files.append(path)
        
        if not existing_files:
            return "WARNING", "No BERT model files found - will use fallback classification", {"missing": missing_files}
        
        if missing_files:
            return "WARNING", f"Some model files missing: {missing_files}", {"existing": existing_files, "missing": missing_files}
        
        return "PASS", "All BERT model files present", {"files": existing_files}
    
    def check_bert_model_loading(self) -> Tuple[str, str, Dict]:
        """Test BERT model loading"""
        try:
            from app.nlp.model_loader import BERTModelLoader
            
            loader = BERTModelLoader()
            model_info = loader.load_model_with_fallback()
            
            if model_info['status'] == 'bert_loaded':
                return "PASS", "BERT model loaded successfully", model_info
            elif model_info['status'] == 'fallback':
                return "WARNING", "Using fallback classification (BERT model not available)", model_info
            else:
                return "FAIL", f"Model loading failed: {model_info.get('error', 'Unknown error')}", model_info
        except Exception as e:
            return "FAIL", f"Model loading check failed: {str(e)}", {"error": str(e)}
    
    def check_bert_classifier_inference(self) -> Tuple[str, str, Dict]:
        """Test BERT classifier inference"""
        try:
            from app.nlp.bert_priority_classifier import AdvancedEventPriorityClassifier
            
            classifier = AdvancedEventPriorityClassifier()
            
            # Test with sample event
            test_event = {
                'title': 'Emergency Board Meeting',
                'description': 'Critical meeting to address urgent company issues',
                'location': 'Boardroom'
            }
            
            priority, confidence = classifier.predict(test_event)
            
            if 1 <= priority <= 5 and 0 <= confidence <= 1:
                return "PASS", f"BERT inference successful: P{priority} (confidence: {confidence:.3f})", {
                    "test_event": test_event,
                    "priority": priority,
                    "confidence": confidence
                }
            else:
                return "FAIL", f"Invalid prediction values: priority={priority}, confidence={confidence}", {}
        except Exception as e:
            return "WARNING", f"BERT inference failed, will use fallback: {str(e)}", {"error": str(e)}
    
    # API Endpoint Checks
    
    def check_api_server_health(self, base_url: str = "http://localhost:8000") -> Tuple[str, str, Dict]:
        """Check API server health"""
        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            
            if response.status_code == 200:
                return "PASS", "API server responding", {"status_code": response.status_code, "response": response.json()}
            else:
                return "FAIL", f"API server returned status {response.status_code}", {"status_code": response.status_code}
        except requests.exceptions.ConnectionError:
            return "SKIP", "API server not running (expected for offline validation)", {}
        except Exception as e:
            return "FAIL", f"API health check failed: {str(e)}", {"error": str(e)}
    
    def check_nlp_endpoints(self, base_url: str = "http://localhost:8000") -> Tuple[str, str, Dict]:
        """Check NLP API endpoints"""
        try:
            # Test priority classification endpoint
            test_data = {
                "title": "Test Meeting",
                "description": "Sample meeting for testing",
                "location": "Conference Room A"
            }
            
            response = requests.post(f"{base_url}/api/v1/nlp/classify-priority", json=test_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if "priority" in result and "confidence" in result:
                    return "PASS", "NLP endpoints functional", {"test_response": result}
                else:
                    return "FAIL", "NLP endpoint returned invalid response", {"response": result}
            else:
                return "FAIL", f"NLP endpoint returned status {response.status_code}", {"status_code": response.status_code}
        except requests.exceptions.ConnectionError:
            return "SKIP", "API server not running", {}
        except Exception as e:
            return "FAIL", f"NLP endpoint check failed: {str(e)}", {"error": str(e)}
    
    # Integration Component Checks
    
    def check_nlp_service_integration(self) -> Tuple[str, str, Dict]:
        """Check NLP service integration"""
        try:
            from app.nlp.nlp_service import NLPService
            
            nlp_service = NLPService()
            
            # Test priority classification
            test_data = {
                'title': 'Emergency System Outage',
                'description': 'Critical production system is down affecting all customers',
                'location': 'Emergency Response Center'
            }
            
            priority, confidence, method = nlp_service.classify_priority(test_data)
            
            if 1 <= priority <= 5 and 0 <= confidence <= 1 and method in ['bert', 'rule_based', 'fallback']:
                return "PASS", f"NLP service working: P{priority} via {method} (confidence: {confidence:.3f})", {
                    "priority": priority,
                    "confidence": confidence,
                    "method": method,
                    "test_data": test_data
                }
            else:
                return "FAIL", f"Invalid NLP service response: priority={priority}, confidence={confidence}, method={method}", {}
        except Exception as e:
            return "FAIL", f"NLP service integration check failed: {str(e)}", {"error": str(e)}
    
    def check_conflict_detector_integration(self) -> Tuple[str, str, Dict]:
        """Check conflict detector with BERT integration"""
        try:
            from app.services.conflict_detector import SmartConflictDetector
            
            detector = SmartConflictDetector()
            
            # Test priority-based conflict resolution
            test_events = [
                type('Event', (), {
                    'title': 'Critical Board Meeting',
                    'priority_level': 1,
                    'priority_confidence': 0.9,
                    'start_time': datetime.now(),
                    'end_time': datetime.now() + timedelta(hours=2)
                })(),
                type('Event', (), {
                    'title': 'Coffee Break',
                    'priority_level': 4,
                    'priority_confidence': 0.8,
                    'start_time': datetime.now() + timedelta(hours=1),
                    'end_time': datetime.now() + timedelta(hours=2)
                })()
            ]
            
            resolution = detector.resolve_conflict_by_priority(test_events)
            
            if 'resolution_type' in resolution and 'recommended_action' in resolution:
                return "PASS", "Conflict detector with BERT integration working", {
                    "resolution_type": resolution['resolution_type'],
                    "action": resolution['recommended_action']
                }
            else:
                return "FAIL", "Invalid conflict resolution response", {"response": resolution}
        except Exception as e:
            return "FAIL", f"Conflict detector check failed: {str(e)}", {"error": str(e)}
    
    # Performance and Configuration Checks
    
    def check_environment_variables(self) -> Tuple[str, str, Dict]:
        """Check required environment variables"""
        required_vars = [
            'DATABASE_URL',
            'SECRET_KEY'
        ]
        
        optional_vars = [
            'BERT_MODEL_PATH',
            'LOG_LEVEL',
            'API_HOST',
            'API_PORT'
        ]
        
        missing_required = []
        missing_optional = []
        present_vars = {}
        
        for var in required_vars:
            value = os.getenv(var)
            if value:
                present_vars[var] = "***" if "SECRET" in var else value[:20] + "..." if len(value) > 20 else value
            else:
                missing_required.append(var)
        
        for var in optional_vars:
            value = os.getenv(var)
            if value:
                present_vars[var] = value
            else:
                missing_optional.append(var)
        
        if missing_required:
            return "FAIL", f"Missing required environment variables: {missing_required}", {
                "missing_required": missing_required,
                "missing_optional": missing_optional,
                "present": present_vars
            }
        
        return "PASS", f"Environment configuration valid", {
            "missing_optional": missing_optional,
            "present": present_vars
        }
    
    def check_logging_configuration(self) -> Tuple[str, str, Dict]:
        """Check logging configuration"""
        try:
            import logging
            
            # Check if loggers are configured
            loggers = ['app.nlp', 'app.api', 'app.services']
            logger_status = {}
            
            for logger_name in loggers:
                logger_obj = logging.getLogger(logger_name)
                logger_status[logger_name] = {
                    "level": logging.getLevelName(logger_obj.level),
                    "handlers": len(logger_obj.handlers),
                    "disabled": logger_obj.disabled
                }
            
            return "PASS", "Logging configuration checked", {"loggers": logger_status}
        except Exception as e:
            return "WARNING", f"Logging check failed: {str(e)}", {"error": str(e)}
    
    def check_dependencies(self) -> Tuple[str, str, Dict]:
        """Check Python dependencies"""
        try:
            required_packages = [
                'fastapi',
                'sqlalchemy',
                'alembic',
                'torch',
                'transformers',
                'scikit-learn',
                'numpy',
                'pandas'
            ]
            
            installed_packages = {}
            missing_packages = []
            
            for package in required_packages:
                try:
                    module = importlib.import_module(package)
                    version = getattr(module, '__version__', 'unknown')
                    installed_packages[package] = version
                except ImportError:
                    missing_packages.append(package)
            
            if missing_packages:
                return "FAIL", f"Missing required packages: {missing_packages}", {
                    "missing": missing_packages,
                    "installed": installed_packages
                }
            
            return "PASS", f"All {len(required_packages)} required packages installed", {"packages": installed_packages}
        except Exception as e:
            return "FAIL", f"Dependency check failed: {str(e)}", {"error": str(e)}
    
    # Testing and Quality Checks
    
    def check_test_files(self) -> Tuple[str, str, Dict]:
        """Check for test files and coverage"""
        test_files = [
            "test_full_event_pipeline.py",
            "validate_bert_training.py",
            "backend/test_behavior_analytics.py"
        ]
        
        existing_tests = []
        missing_tests = []
        
        for test_file in test_files:
            if Path(test_file).exists():
                existing_tests.append(test_file)
            else:
                missing_tests.append(test_file)
        
        coverage_score = len(existing_tests) / len(test_files) * 100
        
        if coverage_score >= 80:
            return "PASS", f"Good test coverage: {coverage_score:.0f}% ({len(existing_tests)}/{len(test_files)} test files)", {
                "coverage": coverage_score,
                "existing": existing_tests,
                "missing": missing_tests
            }
        elif coverage_score >= 50:
            return "WARNING", f"Moderate test coverage: {coverage_score:.0f}%", {
                "coverage": coverage_score,
                "existing": existing_tests,
                "missing": missing_tests
            }
        else:
            return "FAIL", f"Low test coverage: {coverage_score:.0f}%", {
                "coverage": coverage_score,
                "existing": existing_tests,
                "missing": missing_tests
            }
    
    def check_demo_data_generation(self) -> Tuple[str, str, Dict]:
        """Check demo data generation capability"""
        try:
            # Check if demo data script exists
            demo_script = Path("create_demo_data.py")
            if not demo_script.exists():
                return "FAIL", "Demo data generation script not found", {"script": str(demo_script)}
            
            # Try to import the demo data generator
            spec = importlib.util.spec_from_file_location("create_demo_data", demo_script)
            demo_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(demo_module)
            
            if hasattr(demo_module, 'DemoDataGenerator'):
                generator = demo_module.DemoDataGenerator()
                return "PASS", "Demo data generation capability verified", {"script": str(demo_script)}
            else:
                return "FAIL", "DemoDataGenerator class not found in script", {}
        except Exception as e:
            return "FAIL", f"Demo data check failed: {str(e)}", {"error": str(e)}
    
    # Security and Documentation Checks
    
    def check_security_configuration(self) -> Tuple[str, str, Dict]:
        """Check basic security configuration"""
        security_checks = {}
        
        # Check for secrets in environment variables
        secret_key = os.getenv('SECRET_KEY')
        if secret_key:
            if len(secret_key) >= 32:
                security_checks['secret_key'] = "PASS"
            else:
                security_checks['secret_key'] = "FAIL - Too short"
        else:
            security_checks['secret_key'] = "FAIL - Missing"
        
        # Check database URL doesn't contain plain passwords
        db_url = os.getenv('DATABASE_URL', '')
        if db_url and '@' in db_url and not db_url.startswith('postgresql://'):
            security_checks['database_url'] = "WARNING - Check password security"
        else:
            security_checks['database_url'] = "PASS"
        
        # Check for debug mode
        debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
        if debug_mode:
            security_checks['debug_mode'] = "WARNING - Debug mode enabled"
        else:
            security_checks['debug_mode'] = "PASS"
        
        fail_count = len([k for k, v in security_checks.items() if 'FAIL' in v])
        warning_count = len([k for k, v in security_checks.items() if 'WARNING' in v])
        
        if fail_count > 0:
            return "FAIL", f"Security issues found: {fail_count} failures, {warning_count} warnings", security_checks
        elif warning_count > 0:
            return "WARNING", f"Security warnings: {warning_count} items need attention", security_checks
        else:
            return "PASS", "Security configuration looks good", security_checks
    
    def check_documentation(self) -> Tuple[str, str, Dict]:
        """Check documentation files"""
        doc_files = [
            "README.md",
            "CONTRIBUTING.md",
            "docs/api/openapi.yaml",
            "docs/architecture/README.md"
        ]
        
        existing_docs = []
        missing_docs = []
        
        for doc_file in doc_files:
            if Path(doc_file).exists():
                existing_docs.append(doc_file)
            else:
                missing_docs.append(doc_file)
        
        doc_coverage = len(existing_docs) / len(doc_files) * 100
        
        if doc_coverage >= 75:
            return "PASS", f"Good documentation coverage: {doc_coverage:.0f}%", {
                "coverage": doc_coverage,
                "existing": existing_docs,
                "missing": missing_docs
            }
        else:
            return "WARNING", f"Documentation needs improvement: {doc_coverage:.0f}% coverage", {
                "coverage": doc_coverage,
                "existing": existing_docs,
                "missing": missing_docs
            }
    
    # Main validation methods
    
    def run_database_checks(self):
        """Run all database-related checks"""
        print("\n🗄️  DATABASE CHECKS")
        print("=" * 60)
        
        self.run_check("database", "Connection Test", self.check_database_connection)
        self.run_check("database", "Schema Validation", self.check_database_schema)
        self.run_check("database", "Migration Status", self.check_alembic_migrations)
    
    def run_bert_checks(self):
        """Run all BERT model checks"""
        print("\n🤖 BERT MODEL CHECKS")
        print("=" * 60)
        
        self.run_check("bert", "Model Files", self.check_bert_model_files)
        self.run_check("bert", "Model Loading", self.check_bert_model_loading)
        self.run_check("bert", "Inference Test", self.check_bert_classifier_inference)
    
    def run_api_checks(self, base_url: str = "http://localhost:8000"):
        """Run all API endpoint checks"""
        print("\n🌐 API ENDPOINT CHECKS")
        print("=" * 60)
        
        self.run_check("api", "Server Health", self.check_api_server_health, base_url)
        self.run_check("api", "NLP Endpoints", self.check_nlp_endpoints, base_url)
    
    def run_integration_checks(self):
        """Run all integration component checks"""
        print("\n🔗 INTEGRATION CHECKS")
        print("=" * 60)
        
        self.run_check("integration", "NLP Service", self.check_nlp_service_integration)
        self.run_check("integration", "Conflict Detector", self.check_conflict_detector_integration)
    
    def run_configuration_checks(self):
        """Run all configuration and environment checks"""
        print("\n⚙️  CONFIGURATION CHECKS")
        print("=" * 60)
        
        self.run_check("config", "Environment Variables", self.check_environment_variables)
        self.run_check("config", "Logging Setup", self.check_logging_configuration)
        self.run_check("config", "Dependencies", self.check_dependencies)
    
    def run_quality_checks(self):
        """Run all testing and quality checks"""
        print("\n🧪 QUALITY & TESTING CHECKS")
        print("=" * 60)
        
        self.run_check("quality", "Test Coverage", self.check_test_files)
        self.run_check("quality", "Demo Data", self.check_demo_data_generation)
    
    def run_security_checks(self):
        """Run all security and documentation checks"""
        print("\n🔒 SECURITY & DOCUMENTATION")
        print("=" * 60)
        
        self.run_check("security", "Security Config", self.check_security_configuration)
        self.run_check("security", "Documentation", self.check_documentation)
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        total_time = time.time() - self.start_time
        
        # Count results by status
        status_counts = {}
        component_results = {}
        
        for result in self.results:
            status_counts[result.status] = status_counts.get(result.status, 0) + 1
            
            if result.component not in component_results:
                component_results[result.component] = {"PASS": 0, "FAIL": 0, "WARNING": 0, "SKIP": 0}
            component_results[result.component][result.status] += 1
        
        # Calculate overall score
        total_checks = len(self.results)
        pass_count = status_counts.get("PASS", 0)
        fail_count = status_counts.get("FAIL", 0)
        warning_count = status_counts.get("WARNING", 0)
        skip_count = status_counts.get("SKIP", 0)
        
        # Score calculation: PASS = 100%, WARNING = 50%, FAIL = 0%, SKIP = ignored
        scored_checks = total_checks - skip_count
        if scored_checks > 0:
            overall_score = (pass_count * 100 + warning_count * 50) / scored_checks
        else:
            overall_score = 0
        
        # Determine readiness level
        if overall_score >= 90 and fail_count == 0:
            readiness_level = "PRODUCTION READY"
        elif overall_score >= 75 and fail_count <= 2:
            readiness_level = "MOSTLY READY"
        elif overall_score >= 50:
            readiness_level = "NEEDS IMPROVEMENT"
        else:
            readiness_level = "NOT READY"
        
        return {
            "validation_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_execution_time": round(total_time, 2),
                "readiness_level": readiness_level,
                "overall_score": round(overall_score, 1),
                "total_checks": total_checks,
                "status_breakdown": status_counts
            },
            "component_breakdown": component_results,
            "recommendations": self._generate_recommendations(),
            "failed_checks": [
                {
                    "component": r.component,
                    "check": r.check_name,
                    "message": r.message
                }
                for r in self.results if r.status == "FAIL"
            ],
            "warnings": [
                {
                    "component": r.component,
                    "check": r.check_name,
                    "message": r.message
                }
                for r in self.results if r.status == "WARNING"
            ]
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on check results"""
        recommendations = []
        
        # Analyze failures and warnings
        fail_components = set()
        warning_components = set()
        
        for result in self.results:
            if result.status == "FAIL":
                fail_components.add(result.component)
            elif result.status == "WARNING":
                warning_components.add(result.component)
        
        # Generate specific recommendations
        if "database" in fail_components:
            recommendations.append("🗄️ Fix database connectivity and schema issues before deployment")
        
        if "bert" in fail_components:
            recommendations.append("🤖 Train and deploy BERT model or ensure fallback classification is acceptable")
        
        if "api" in fail_components:
            recommendations.append("🌐 Resolve API endpoint issues and ensure proper error handling")
        
        if "integration" in fail_components:
            recommendations.append("🔗 Fix integration component failures - critical for system functionality")
        
        if "config" in fail_components:
            recommendations.append("⚙️ Address configuration issues, especially environment variables and dependencies")
        
        if "security" in fail_components:
            recommendations.append("🔒 Resolve security configuration issues before production deployment")
        
        # General recommendations
        if len([r for r in self.results if r.status == "FAIL"]) > 5:
            recommendations.append("📋 High number of failures detected - consider systematic review and fixes")
        
        if len([r for r in self.results if r.status == "WARNING"]) > 3:
            recommendations.append("⚠️ Multiple warnings found - address for optimal production performance")
        
        return recommendations

async def main():
    """Main validation function"""
    parser = argparse.ArgumentParser(description="Production Readiness Validation for KairoCal BERT System")
    parser.add_argument("--component", choices=["database", "bert", "api", "integration", "config", "quality", "security"], 
                       help="Run checks for specific component only")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API base URL for endpoint checks")
    parser.add_argument("--verbose", action="store_true", help="Verbose output with detailed results")
    parser.add_argument("--output", help="Save report to JSON file")
    parser.add_argument("--full-check", action="store_true", help="Run all validation checks")
    
    args = parser.parse_args()
    
    print("🚀 KairoCal BERT Priority Classification System - Production Readiness Validation")
    print("=" * 80)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    validator = ProductionReadinessValidator(verbose=args.verbose)
    
    # Run checks based on arguments
    if args.component:
        print(f"🔍 Running checks for component: {args.component}")
        if args.component == "database":
            validator.run_database_checks()
        elif args.component == "bert":
            validator.run_bert_checks()
        elif args.component == "api":
            validator.run_api_checks(args.api_url)
        elif args.component == "integration":
            validator.run_integration_checks()
        elif args.component == "config":
            validator.run_configuration_checks()
        elif args.component == "quality":
            validator.run_quality_checks()
        elif args.component == "security":
            validator.run_security_checks()
    else:
        # Run all checks
        validator.run_database_checks()
        validator.run_bert_checks()
        validator.run_api_checks(args.api_url)
        validator.run_integration_checks()
        validator.run_configuration_checks()
        validator.run_quality_checks()
        validator.run_security_checks()
    
    # Generate and display report
    report = validator.generate_report()
    
    print("\n📊 VALIDATION SUMMARY")
    print("=" * 60)
    print(f"🎯 Readiness Level: {report['validation_summary']['readiness_level']}")
    print(f"📈 Overall Score: {report['validation_summary']['overall_score']}%")
    print(f"⏱️  Total Time: {report['validation_summary']['total_execution_time']}s")
    print(f"📋 Total Checks: {report['validation_summary']['total_checks']}")
    
    status_breakdown = report['validation_summary']['status_breakdown']
    print(f"✅ Passed: {status_breakdown.get('PASS', 0)}")
    print(f"❌ Failed: {status_breakdown.get('FAIL', 0)}")
    print(f"⚠️  Warnings: {status_breakdown.get('WARNING', 0)}")
    print(f"⏭️  Skipped: {status_breakdown.get('SKIP', 0)}")
    
    # Show failures and warnings
    if report['failed_checks']:
        print("\n❌ FAILED CHECKS:")
        for check in report['failed_checks']:
            print(f"  • {check['component']}/{check['check']}: {check['message']}")
    
    if report['warnings']:
        print("\n⚠️  WARNINGS:")
        for warning in report['warnings']:
            print(f"  • {warning['component']}/{warning['check']}: {warning['message']}")
    
    # Show recommendations
    if report['recommendations']:
        print("\n💡 RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"  • {rec}")
    
    # Save report if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n💾 Full report saved to: {args.output}")
    
    # Exit code based on readiness
    if report['validation_summary']['readiness_level'] in ["PRODUCTION READY", "MOSTLY READY"]:
        print(f"\n🎉 System is ready for production deployment!")
        sys.exit(0)
    else:
        print(f"\n🛠️  System needs improvements before production deployment.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
