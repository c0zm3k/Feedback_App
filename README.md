# Student Feedback System

A comprehensive web-based feedback system built with Streamlit and SQLite, designed for educational institutions to collect and manage student feedback for teachers.

## Features

### 🎯 Core Features
- **Multi-User System**: Separate interfaces for Admin, Teachers, and Students
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Real-time Feedback**: Automatic timestamp recording for all feedback submissions
- **Word Count Validation**: Ensures feedback quality with minimum 30-word requirement
- **Secure Authentication**: Password-protected admin and teacher logins

### 👨‍💼 Admin Dashboard
- Add new teachers with complete profiles
- View all registered teachers
- Monitor feedback statistics for each teacher
- Delete teachers and their associated feedback
- Default admin credentials: `admin` / `admin123`

### 👩‍🏫 Teacher Dashboard
- View personal information and teaching details
- Access all feedback from students
- Real-time feedback display with timestamps
- Clean, organized feedback presentation

### 📝 Student Feedback
- No login required for students
- Select teacher from dropdown menu
- Submit detailed feedback with name
- Word count validation (minimum 30 words)
- Instant submission confirmation

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd student-feedback-system
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - The application will start automatically

## Usage Guide

### For Administrators
1. Click "Admin Login" on the home page
2. Use default credentials: `admin` / `admin123`
3. Add new teachers using the "Add New Teacher" form
4. View all teachers and their feedback statistics
5. Manage teachers (add/delete) as needed

### For Teachers
1. Click "Teacher Login" on the home page
2. Enter your username and password (provided by admin)
3. View your personal dashboard with all student feedback
4. Monitor feedback trends and student responses

### For Students
1. Click "Give Feedback" on the home page
2. Select your teacher from the dropdown menu
3. Enter your full name
4. Write detailed feedback (minimum 30 words)
5. Submit and receive confirmation

## Database Structure

The system uses SQLite with three main tables:

### Admins Table
- `id`: Primary key
- `username`: Admin username
- `password_hash`: Hashed password
- `created_at`: Account creation timestamp

### Teachers Table
- `id`: Primary key
- `username`: Teacher username
- `password_hash`: Hashed password
- `full_name`: Teacher's full name
- `email`: Teacher's email address
- `subject`: Subject taught
- `created_at`: Account creation timestamp

### Feedback Table
- `id`: Primary key
- `teacher_id`: Foreign key to teachers table
- `student_name`: Student's name
- `feedback_text`: Feedback content
- `submission_time`: Automatic timestamp

## Security Features

- **Password Hashing**: All passwords are hashed using SHA-256
- **Session Management**: Secure session handling for logged-in users
- **Input Validation**: Comprehensive validation for all user inputs
- **SQL Injection Protection**: Parameterized queries prevent SQL injection

## Customization

### Changing Default Admin Credentials
Edit the `database.py` file and modify the default admin credentials in the `init_database()` method.

### Styling Customization
The application uses custom CSS for styling. Modify the CSS in the `main.py` file to change colors, layouts, and responsive behavior.

### Database Location
The SQLite database file (`feedback_system.db`) is created in the same directory as the application. You can change the database path in the `DatabaseManager` class.

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port: `streamlit run main.py --server.port 8502`

2. **Database errors**
   - Delete the `feedback_system.db` file and restart the application

3. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

4. **Mobile responsiveness issues**
   - Clear browser cache and refresh the page

## Future Enhancements

- [ ] Student login system
- [ ] Email notifications for new feedback
- [ ] Feedback analytics and reports
- [ ] Export functionality (PDF/Excel)
- [ ] Multi-language support
- [ ] Advanced search and filtering
- [ ] Feedback categories and ratings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please create an issue in the repository or contact the development team.

---

**Note**: This is a development version. For production use, consider implementing additional security measures and backup systems.
