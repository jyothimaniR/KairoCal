#!/usr/bin/env python3
"""
Pre-Training Environment Check for KairoCal BERT Model
Verifies all dependencies and system requirements before training
"""

import sys
import os
import json
import platform
import subprocess
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TrainingEnvironmentChecker:
    """Comprehensive pre-training environment validation"""
    
    def __init__(self):
        self.checks = []
        self.warnings = []
        self.errors = []
        
    def log_check(self, name: str, status: str, message: str, details=None):
        """Log a check result"""
        result = {
            "check": name,
            "status": status,  # "PASS", "FAIL", "WARNING"
            "message": message,
            "details": details or {}
        }
        self.checks.append(result)
        
        # Color coding for terminal output
        color_map = {
            "PASS": "\033[92m",     # Green
            "FAIL": "\033[91m",     # Red
            "WARNING": "\033[93m"   # Yellow
        }
        reset_color = "\033[0m"
        
        status_colored = f"{color_map.get(status, '')}{status}{reset_color}"
        print(f"  {status_colored:15} {name:40} {message}")
        
        if details:
            for key, value in details.items():
                print(f"    {key}: {value}")
    
    def check_python_version(self):
        """Check Python version compatibility"""
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        if version >= (3, 8):
            self.log_check(
                "Python Version", 
                "PASS", 
                f"Python {version_str} is compatible",
                {"required": "3.8+", "actual": version_str}
            )
        else:
            self.log_check(
                "Python Version", 
                "FAIL", 
                f"Python {version_str} is too old",
                {"required": "3.8+", "actual": version_str}
            )
    
    def check_dependencies(self):
        """Check all required dependencies"""
        required_packages = {
            'torch': 'PyTorch for neural networks',
            'transformers': 'HuggingFace Transformers for BERT',
            'scikit-learn': 'Machine learning utilities',
            'numpy': 'Numerical computing',
            'pandas': 'Data manipulation',
            'fastapi': 'API framework',
            'sqlalchemy': 'Database ORM'
        }
        
        installed = {}
        missing = []
        
        for package, description in required_packages.items():
            try:
                if package == 'scikit-learn':
                    module = __import__('sklearn')
                else:
                    module = __import__(package.replace('-', '_'))
                version = getattr(module, '__version__', 'unknown')
                installed[package] = version
            except ImportError:
                missing.append(package)
        
        if not missing:
            self.log_check(
                "Dependencies", 
                "PASS", 
                f"All {len(required_packages)} packages installed",
                installed
            )
        else:
            self.log_check(
                "Dependencies", 
                "FAIL", 
                f"Missing packages: {', '.join(missing)}",
                {"installed": installed, "missing": missing}
            )
    
    def check_gpu_availability(self):
        """Check GPU and CUDA availability"""
        try:
            import torch
            
            cuda_available = torch.cuda.is_available()
            device_count = torch.cuda.device_count() if cuda_available else 0
            
            if cuda_available:
                gpu_name = torch.cuda.get_device_name(0) if device_count > 0 else "Unknown"
                gpu_memory = torch.cuda.get_device_properties(0).total_memory // (1024**3) if device_count > 0 else 0
                
                self.log_check(
                    "GPU/CUDA", 
                    "PASS", 
                    f"CUDA available with {device_count} GPU(s)",
                    {
                        "gpu_name": gpu_name,
                        "gpu_memory_gb": gpu_memory,
                        "cuda_version": torch.version.cuda,
                        "torch_version": torch.__version__
                    }
                )
            else:
                self.log_check(
                    "GPU/CUDA", 
                    "WARNING", 
                    "No CUDA GPU detected, training will use CPU",
                    {
                        "torch_version": torch.__version__,
                        "cuda_compiled": torch.version.cuda,
                        "recommendation": "Training will be slower on CPU"
                    }
                )
                
        except ImportError:
            self.log_check(
                "GPU/CUDA", 
                "FAIL", 
                "PyTorch not installed, cannot check GPU",
                {}
            )
    
    def check_model_directories(self):
        """Check and create model directories"""
        model_dirs = [
            "models",
            "models/bert_priority_classifier",
            "models/training_data",
            "models/logs"
        ]
        
        created_dirs = []
        existing_dirs = []
        
        for dir_path in model_dirs:
            full_path = Path(dir_path)
            if full_path.exists():
                existing_dirs.append(dir_path)
            else:
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(dir_path)
                except Exception as e:
                    self.log_check(
                        "Model Directories", 
                        "FAIL", 
                        f"Failed to create {dir_path}: {str(e)}",
                        {}
                    )
                    return
        
        self.log_check(
            "Model Directories", 
            "PASS", 
            f"Model directories ready",
            {
                "existing": existing_dirs,
                "created": created_dirs,
                "total_dirs": len(model_dirs)
            }
        )
    
    def check_training_data_generator(self):
        """Test training data generation"""
        try:
            # Import training components
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            
            # Check if we can import the training module
            from train_bert_model import BERTTrainingDataGenerator
            
            # Test data generation
            generator = BERTTrainingDataGenerator()
            sample_data = generator.generate_training_dataset(size=10)
            
            if len(sample_data) == 10:
                # Check data structure
                sample = sample_data[0]
                required_fields = ['title', 'description', 'priority']
                
                if all(field in sample for field in required_fields):
                    self.log_check(
                        "Training Data Generator", 
                        "PASS", 
                        f"Generated {len(sample_data)} samples successfully",
                        {
                            "sample_count": len(sample_data),
                            "sample_fields": list(sample.keys()),
                            "priority_distribution": self._analyze_priority_distribution(sample_data)
                        }
                    )
                else:
                    missing_fields = [f for f in required_fields if f not in sample]
                    self.log_check(
                        "Training Data Generator", 
                        "FAIL", 
                        f"Missing required fields: {missing_fields}",
                        {"available_fields": list(sample.keys())}
                    )
            else:
                self.log_check(
                    "Training Data Generator", 
                    "FAIL", 
                    f"Expected 10 samples, got {len(sample_data)}",
                    {}
                )
                
        except ImportError as e:
            self.log_check(
                "Training Data Generator", 
                "FAIL", 
                f"Cannot import training module: {str(e)}",
                {}
            )
        except Exception as e:
            self.log_check(
                "Training Data Generator", 
                "FAIL", 
                f"Data generation failed: {str(e)}",
                {}
            )
    
    def _analyze_priority_distribution(self, data):
        """Analyze priority distribution in training data"""
        priority_counts = {}
        for item in data:
            priority = item.get('priority', 0)
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        return priority_counts
    
    def check_system_specs(self):
        """Check system specifications for training"""
        try:
            import psutil
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_gb = memory.total / (1024**3)
            memory_available_gb = memory.available / (1024**3)
            
            # CPU info
            cpu_count = psutil.cpu_count()
            cpu_count_physical = psutil.cpu_count(logical=False)
            
            # Disk space
            disk = psutil.disk_usage('.')
            disk_free_gb = disk.free / (1024**3)
            
            specs = {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "cpu_cores_logical": cpu_count,
                "cpu_cores_physical": cpu_count_physical,
                "memory_total_gb": round(memory_gb, 2),
                "memory_available_gb": round(memory_available_gb, 2),
                "disk_free_gb": round(disk_free_gb, 2)
            }
            
            # Check if specs are adequate
            status = "PASS"
            message = "System specs adequate for training"
            
            if memory_gb < 8:
                status = "WARNING"
                message = f"Low memory ({memory_gb:.1f}GB), training may be slow"
            elif memory_gb < 4:
                status = "FAIL"
                message = f"Insufficient memory ({memory_gb:.1f}GB), training likely to fail"
            
            if disk_free_gb < 2:
                status = "WARNING"
                message = f"Low disk space ({disk_free_gb:.1f}GB), may not have room for models"
            
            self.log_check(
                "System Specifications", 
                status, 
                message,
                specs
            )
            
        except ImportError:
            self.log_check(
                "System Specifications", 
                "WARNING", 
                "psutil not available, cannot check system specs",
                {
                    "platform": platform.system(),
                    "python_version": platform.python_version()
                }
            )
    
    def check_existing_models(self):
        """Check for existing trained models"""
        model_path = Path("models/bert_priority_classifier")
        
        if model_path.exists():
            model_files = list(model_path.glob("*"))
            if model_files:
                self.log_check(
                    "Existing Models", 
                    "WARNING", 
                    f"Found existing model files, training will overwrite",
                    {
                        "model_directory": str(model_path),
                        "existing_files": [f.name for f in model_files],
                        "file_count": len(model_files)
                    }
                )
            else:
                self.log_check(
                    "Existing Models", 
                    "PASS", 
                    "Model directory exists but empty, ready for training",
                    {}
                )
        else:
            self.log_check(
                "Existing Models", 
                "PASS", 
                "No existing models found, ready for fresh training",
                {}
            )
    
    def run_all_checks(self):
        """Run all environment checks"""
        print("🔍 KairoCal BERT Training Environment Check")
        print("=" * 70)
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all checks
        self.check_python_version()
        self.check_dependencies()
        self.check_gpu_availability()
        self.check_model_directories()
        self.check_training_data_generator()
        self.check_system_specs()
        self.check_existing_models()
        
        # Summary
        passed = len([c for c in self.checks if c['status'] == 'PASS'])
        failed = len([c for c in self.checks if c['status'] == 'FAIL'])
        warnings = len([c for c in self.checks if c['status'] == 'WARNING'])
        
        print()
        print("📊 ENVIRONMENT CHECK SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"📋 Total Checks: {len(self.checks)}")
        
        # Determine readiness
        if failed == 0:
            if warnings == 0:
                readiness = "FULLY READY"
                print(f"\n🎉 Environment is {readiness} for BERT training!")
            else:
                readiness = "READY WITH WARNINGS"
                print(f"\n✅ Environment is {readiness} for BERT training!")
                print("⚠️  Check warnings above for potential issues.")
        else:
            readiness = "NOT READY"
            print(f"\n❌ Environment is {readiness} for BERT training!")
            print("🛠️  Please fix failed checks before proceeding.")
        
        # Show failed checks
        if failed > 0:
            print("\n❌ FAILED CHECKS:")
            for check in self.checks:
                if check['status'] == 'FAIL':
                    print(f"  • {check['check']}: {check['message']}")
        
        # Show warnings
        if warnings > 0:
            print("\n⚠️  WARNINGS:")
            for check in self.checks:
                if check['status'] == 'WARNING':
                    print(f"  • {check['check']}: {check['message']}")
        
        # Save detailed report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"environment_check_report_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "readiness": readiness,
            "summary": {
                "passed": passed,
                "failed": failed,
                "warnings": warnings,
                "total": len(self.checks)
            },
            "checks": self.checks
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"\n💾 Detailed report saved to: {report_file}")
        except Exception as e:
            print(f"\n⚠️  Failed to save report: {str(e)}")
        
        # Return readiness status
        return failed == 0

def main():
    """Main entry point"""
    checker = TrainingEnvironmentChecker()
    is_ready = checker.run_all_checks()
    
    if is_ready:
        print("\n🚀 Ready to proceed with BERT model training!")
        print("   Next step: python train_bert_model.py")
        sys.exit(0)
    else:
        print("\n🛠️  Please resolve environment issues before training.")
        sys.exit(1)

if __name__ == "__main__":
    main()
