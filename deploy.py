#!/usr/bin/env python3
"""
Deployment Helper Script for Student Feedback System
This script helps prepare your project for Streamlit Cloud deployment
"""

import os
import subprocess
import sys

def check_git_status():
    """Check if git is initialized and files are committed"""
    print("🔍 Checking Git status...")
    
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git repository not initialized")
            return False
        
        # Check if there are uncommitted changes
        result = subprocess.run(['git', 'diff', '--name-only'], capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  There are uncommitted changes:")
            print(result.stdout)
            return False
        
        print("✅ Git repository is ready")
        return True
        
    except FileNotFoundError:
        print("❌ Git is not installed")
        return False

def check_required_files():
    """Check if all required files exist"""
    print("\n📁 Checking required files...")
    
    required_files = [
        'main.py',
        'database.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def test_application():
    """Test if the application can run"""
    print("\n🧪 Testing application...")
    
    try:
        # Test imports
        import streamlit
        from database import DatabaseManager
        
        # Test database initialization
        db = DatabaseManager("test_deploy.db")
        print("✅ Application imports and database initialization successful")
        
        # Clean up test database
        if os.path.exists("test_deploy.db"):
            os.remove("test_deploy.db")
        
        return True
        
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def create_deployment_instructions():
    """Create deployment instructions"""
    print("\n📋 Deployment Instructions:")
    print("=" * 50)
    print("1. Push to GitHub/GitLab:")
    print("   git add .")
    print("   git commit -m 'Ready for deployment'")
    print("   git push origin main")
    print()
    print("2. Deploy on Streamlit Cloud:")
    print("   - Go to: https://share.streamlit.io/")
    print("   - Sign in with GitHub/GitLab")
    print("   - Click 'New app'")
    print("   - Select your repository")
    print("   - Set main file path: main.py")
    print("   - Click 'Deploy!'")
    print()
    print("3. Your app will be available at:")
    print("   https://your-app-name.streamlit.app")

def main():
    """Main deployment check function"""
    print("🚀 Student Feedback System - Deployment Check")
    print("=" * 50)
    
    # Check all requirements
    git_ready = check_git_status()
    files_ready = check_required_files()
    app_ready = test_application()
    
    print("\n" + "=" * 50)
    
    if git_ready and files_ready and app_ready:
        print("🎉 All checks passed! Your app is ready for deployment!")
        create_deployment_instructions()
    else:
        print("❌ Some checks failed. Please fix the issues above before deploying.")
        print("\nCommon fixes:")
        print("- Initialize git: git init")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Commit changes: git add . && git commit -m 'Initial commit'")

if __name__ == "__main__":
    main()
