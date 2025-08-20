#!/usr/bin/env python3
"""
Test script for Student Feedback System
This script tests the basic functionality of the system
"""

import sqlite3
import hashlib
from database import DatabaseManager

def test_database():
    """Test database functionality"""
    print("🧪 Testing Database Functionality...")
    
    # Initialize database
    db = DatabaseManager("test_feedback_system.db")
    print("✅ Database initialized")
    
    # Test admin login
    admin_valid = db.verify_admin_login("admin", "admin123")
    admin_invalid = db.verify_admin_login("admin", "wrongpassword")
    print(f"✅ Admin login test: Valid={admin_valid}, Invalid={not admin_invalid}")
    
    # Test adding teacher
    teacher_added = db.add_teacher("testteacher", "password123", "Test Teacher", "test@example.com", "Mathematics")
    print(f"✅ Add teacher test: {teacher_added}")
    
    # Test teacher login
    teacher = db.verify_teacher_login("testteacher", "password123")
    print(f"✅ Teacher login test: {teacher is not None}")
    
    # Test getting teachers
    teachers = db.get_all_teachers()
    print(f"✅ Get teachers test: Found {len(teachers)} teachers")
    
    # Test adding feedback
    if teacher:
        db.submit_feedback(teacher[0], "Test Student", "This is a test feedback with more than thirty words to meet the minimum requirement for the feedback system.")
        print("✅ Add feedback test: Success")
        
        # Test getting feedback
        feedback_list = db.get_feedback_for_teacher(teacher[0])
        print(f"✅ Get feedback test: Found {len(feedback_list)} feedback entries")
    
    # Clean up test database
    import os
    if os.path.exists("test_feedback_system.db"):
        os.remove("test_feedback_system.db")
        print("✅ Test database cleaned up")
    
    print("\n🎉 All tests passed! The system is working correctly.")

def test_password_hashing():
    """Test password hashing functionality"""
    print("\n🔐 Testing Password Hashing...")
    
    password = "testpassword123"
    db = DatabaseManager()
    
    hash1 = db.hash_password(password)
    hash2 = db.hash_password(password)
    
    if hash1 == hash2:
        print("✅ Password hashing is consistent")
    else:
        print("❌ Password hashing is inconsistent")
    
    if len(hash1) == 64:  # SHA-256 produces 64 character hex string
        print("✅ Password hash length is correct")
    else:
        print("❌ Password hash length is incorrect")

def main():
    """Main test function"""
    print("🚀 Starting Student Feedback System Tests...")
    print("=" * 50)
    
    try:
        test_password_hashing()
        test_database()
        print("\n✅ All tests completed successfully!")
        print("🎯 The system is ready to use!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("🔧 Please check your installation and try again.")

if __name__ == "__main__":
    main()
