# Quick Start Guide - Student Feedback System

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
# Windows
py -m pip install -r requirements.txt

# Mac/Linux
pip3 install -r requirements.txt
```

### Step 2: Run the Application
```bash
# Windows - Double click run.bat or use:
py -m streamlit run main.py

# Mac/Linux - Use:
./run.sh
# or
streamlit run main.py
```

### Step 3: Access the System
- Open your browser and go to: `http://localhost:8501`
- The application will start automatically

## 🔑 Default Login Credentials

### Admin Access
- **Username:** `admin`
- **Password:** `admin123`

## 📱 How to Use

### For Administrators
1. Click "Admin Login" → Login with admin/admin123
2. Add teachers using the "Add New Teacher" form
3. View all teachers and their feedback statistics

### For Teachers
1. Click "Teacher Login" → Login with credentials provided by admin
2. View your personal dashboard with student feedback
3. Monitor feedback trends

### For Students
1. Click "Give Feedback" (no login required)
2. Select your teacher from the dropdown
3. Enter your name and detailed feedback (minimum 30 words)
4. Submit and receive confirmation

## 🎯 Key Features

✅ **Responsive Design** - Works on mobile, tablet, and desktop  
✅ **Real-time Timestamps** - Automatic date/time recording  
✅ **Word Count Validation** - Ensures quality feedback (30+ words)  
✅ **Secure Authentication** - Password-protected admin/teacher access  
✅ **Individual Teacher Databases** - Each teacher sees only their feedback  
✅ **No Sidebar** - Clean, modern interface  
✅ **Automatic Redirects** - Seamless navigation after login  

## 🔧 Troubleshooting

**Port already in use?**
```bash
py -m streamlit run main.py --server.port 8502
```

**Database issues?**
- Delete `feedback_system.db` and restart

**Import errors?**
- Run: `py -m pip install -r requirements.txt`

## 📞 Support

- Check the full README.md for detailed documentation
- Run `py test_system.py` to verify system functionality
- All files are well-commented for easy customization

---

**Ready to collect feedback! 🎉**
