"""
Configuration file for Student Feedback System
Modify these settings to customize the application behavior
"""

# Application Settings
APP_TITLE = "Student Feedback System"
APP_ICON = "📝"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "collapsed"

# Database Settings
DATABASE_PATH = "feedback_system.db"

# Default Admin Credentials
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

# Feedback Settings
MIN_WORD_COUNT = 30
MAX_WORD_COUNT = 1000

# UI Colors and Styling
PRIMARY_COLOR = "#667eea"
SECONDARY_COLOR = "#764ba2"
SUCCESS_COLOR = "#28a745"
ERROR_COLOR = "#dc3545"
WARNING_COLOR = "#ffc107"

# Responsive Design Breakpoints
MOBILE_BREAKPOINT = 768
TABLET_BREAKPOINT = 1024

# Session Timeout (in seconds)
SESSION_TIMEOUT = 3600  # 1 hour

# File Upload Settings (for future use)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_FILE_TYPES = ['.pdf', '.doc', '.docx', '.txt']

# Email Settings (for future use)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ENABLED = False

# Security Settings
PASSWORD_MIN_LENGTH = 6
PASSWORD_REQUIRE_SPECIAL_CHARS = False
LOGIN_ATTEMPT_LIMIT = 5
LOGIN_LOCKOUT_DURATION = 300  # 5 minutes

# Export Settings (for future use)
EXPORT_FORMATS = ['csv', 'pdf', 'excel']
EXPORT_MAX_RECORDS = 1000
