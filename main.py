import streamlit as st
import streamlit.components.v1 as components
from database import DatabaseManager
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Student Feedback System",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/your-username/student-feedback-system',
        'Report a bug': 'https://github.com/your-username/student-feedback-system/issues',
        'About': 'Student Feedback System - A comprehensive web-based feedback system for educational institutions.'
    }
)

# Initialize database
db = DatabaseManager()

# Custom CSS for responsive design
st.markdown("""
<style>
    body { background-color: #0f1116; }
    .main-header {
        background: linear-gradient(90deg, #1f2937 0%, #111827 100%);
        padding: 2rem;
        border-radius: 10px;
        color: #e5e7eb;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #374151;
    }
    .login-container, .feedback-form, .dashboard-card {
        background: #111827;
        color: #e5e7eb;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        margin: 1rem 0;
        border: 1px solid #374151;
    }
    .dashboard-card { border-left: 4px solid #6366f1; }
    .nav-buttons { display: flex; justify-content: center; gap: 1rem; margin: 2rem 0; flex-wrap: wrap; }
    .nav-button, .stButton>button {
        background: linear-gradient(45deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        padding: 0.75rem 1.25rem !important;
        border-radius: 9999px !important;
        font-weight: 600 !important;
        border: none !important;
        cursor: pointer !important;
    }
    .nav-button:hover, .stButton>button:hover { filter: brightness(1.1); }
    .success-message { background: #064e3b; color: #d1fae5; border: 1px solid #10b981; }
    .error-message { background: #450a0a; color: #fecaca; border: 1px solid #ef4444; }
    .stTextInput>div>div>input, textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #0b1220 !important;
        color: #e5e7eb !important;
        border-color: #374151 !important;
    }
    .stMarkdown, .stText, label, .stRadio label, .stSelectbox label { color: #e5e7eb !important; }
    .quick-links { display: flex; justify-content: center; gap: 0.5rem; margin: 0 0 1rem 0; flex-wrap: wrap; }
    .quick-links .nav-button { padding: 0.5rem 1rem !important; text-decoration: none !important; display: inline-block; }
    @media (max-width: 768px) {
        .nav-buttons { flex-direction: column; align-items: center; }
        .nav-button { width: 100%; max-width: 300px; }
        .login-container { margin: 1rem; padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

def _get_query_params_safe():
    """Return query params as a plain dict, supporting both stable and experimental APIs."""
    try:
        # Newer Streamlit versions
        return dict(st.query_params)
    except Exception:
        try:
            # Older Streamlit 1.x
            return st.experimental_get_query_params()
        except Exception:
            return {}

def _set_query_params_safe(**params):
    """Set query params, supporting both stable and experimental APIs."""
    try:
        st.query_params.clear()
        for k, v in params.items():
            st.query_params[k] = v
    except Exception:
        try:
            st.experimental_set_query_params(**params)
        except Exception:
            pass

def navigate_to(page: str):
    """Set the target page, sync it to the URL, and rerun for an immediate redirect."""
    st.session_state.current_page = page
    qp = _get_query_params_safe()
    if qp.get("page") != page:
        _set_query_params_safe(page=page)
    st.rerun()

def render_quick_links():
    """Render top quick links for primary actions."""
    st.markdown(
        '<div class="quick-links">\n'
        '  <a class="nav-button" href="?page=admin_login">👨‍💼 Admin Login</a>\n'
        '  <a class="nav-button" href="?page=teacher_login">👩‍🏫 Teacher Login</a>\n'
        '  <a class="nav-button" href="?page=student_feedback">📝 Give Feedback</a>\n'
        '</div>',
        unsafe_allow_html=True,
    )

def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if 'teacher_logged_in' not in st.session_state:
        st.session_state.teacher_logged_in = False
    if 'current_teacher' not in st.session_state:
        st.session_state.current_teacher = None

    # Read desired page from URL if present
    page_from_url = _get_query_params_safe().get("page")
    allowed_pages = {
        'home', 'admin_login', 'teacher_login', 'student_feedback',
        'admin_dashboard', 'teacher_dashboard', 'thank_you'
    }
    if page_from_url and page_from_url in allowed_pages and page_from_url != st.session_state.current_page:
        st.session_state.current_page = page_from_url

    # Header
    st.markdown('<div class="main-header"><h1>📝 Student Feedback System</h1></div>', unsafe_allow_html=True)

    # Global quick links
    render_quick_links()

    # Navigation
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'admin_login':
        show_admin_login()
    elif st.session_state.current_page == 'teacher_login':
        show_teacher_login()
    elif st.session_state.current_page == 'student_feedback':
        show_student_feedback()
    elif st.session_state.current_page == 'admin_dashboard':
        show_admin_dashboard()
    elif st.session_state.current_page == 'teacher_dashboard':
        show_teacher_dashboard()
    elif st.session_state.current_page == 'thank_you':
        show_thank_you_page()

def show_home_page():
    st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👨‍💼 Admin Login", key="admin_nav", use_container_width=True):
            navigate_to('admin_login')
    
    with col2:
        if st.button("👩‍🏫 Teacher Login", key="teacher_nav", use_container_width=True):
            navigate_to('teacher_login')
    
    with col3:
        if st.button("📝 Give Feedback", key="feedback_nav", use_container_width=True):
            navigate_to('student_feedback')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="dashboard-card">
        <h2>Welcome to the Student Feedback System</h2>
        <p>This system allows students to provide valuable feedback to their teachers. 
        Teachers can view their feedback, and administrators can manage the system.</p>
        
        <h3>How to use:</h3>
        <ul>
            <li><strong>Students:</strong> Click "Give Feedback" to submit feedback for your teachers</li>
            <li><strong>Teachers:</strong> Click "Teacher Login" to view feedback from your students</li>
            <li><strong>Administrators:</strong> Click "Admin Login" to manage teachers and view all feedback</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def show_admin_login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h2>👨‍💼 Admin Login</h2>', unsafe_allow_html=True)
    
    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if db.verify_admin_login(username, password):
                st.session_state.admin_logged_in = True
                st.success("Login successful! Redirecting to admin dashboard...")
                navigate_to('admin_dashboard')
            else:
                st.error("Invalid username or password!")
    
    if st.button("← Back to Home"):
        navigate_to('home')
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_teacher_login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h2>👩‍🏫 Teacher Login</h2>', unsafe_allow_html=True)
    
    with st.form("teacher_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            teacher = db.verify_teacher_login(username, password)
            if teacher:
                st.session_state.teacher_logged_in = True
                st.session_state.current_teacher = teacher
                st.success("Login successful! Redirecting to teacher dashboard...")
                navigate_to('teacher_dashboard')
            else:
                st.error("Invalid username or password!")
    
    if st.button("← Back to Home"):
        navigate_to('home')
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_student_feedback():
    st.markdown('<div class="feedback-form">', unsafe_allow_html=True)
    st.markdown('<h2>📝 Student Feedback Form</h2>', unsafe_allow_html=True)
    
    # Get all teachers for selection
    teachers = db.get_all_teachers()
    
    if not teachers:
        st.warning("No teachers available. Please contact the administrator.")
        if st.button("← Back to Home"):
            navigate_to('home')
        return
    
    with st.form("feedback_form"):
        # Teacher selection
        teacher_options = {f"{t[2]} ({t[4]})": t[0] for t in teachers}
        selected_teacher_name = st.selectbox("Select Teacher", list(teacher_options.keys()))
        teacher_id = teacher_options[selected_teacher_name]

        # Student ID (instead of name)
        student_id = st.text_input("Your Student ID", placeholder="Enter your Student ID")
        
        # Feedback text
        feedback_text = st.text_area(
            "Your Feedback", 
            placeholder="Please provide your feedback (minimum 30-40 words). Share your thoughts about the teaching style, course content, and suggestions for improvement.",
            height=200
        )
        
        # Live-resolve student name for entered ID
        resolved_name = None
        if student_id.strip():
            sr = db.get_student_by_student_id(teacher_id, student_id.strip())
            if sr:
                resolved_name = sr[3]
                st.success(f"Student: {resolved_name}")
            else:
                st.warning("No student found with this ID for the selected teacher")

        # Word count
        word_count = len(feedback_text.split()) if feedback_text else 0
        st.write(f"Word count: {word_count}")
        
        submit = st.form_submit_button("Submit Feedback")
        
        if submit:
            if not student_id.strip():
                st.error("Please enter your Student ID!")
            elif not feedback_text.strip():
                st.error("Please enter your feedback!")
            elif word_count < 30:
                st.error(f"Feedback must be at least 30 words. Current: {word_count} words")
            else:
                # Validate Student ID belongs to selected teacher
                student_row = db.get_student_by_student_id(teacher_id, student_id.strip())
                if not student_row:
                    st.toast("🤪 Oops! That SID looks funky. Check with your teacher and try again!", icon="🙃")
                else:
                    # Check one submission per day
                    if db.has_student_submitted_today(teacher_id, student_id.strip()):
                        st.warning("You have already submitted feedback today. Please try again tomorrow.")
                        return
                    # Submit feedback
                    ok = db.submit_feedback(teacher_id, student_id.strip(), feedback_text.strip())
                    if ok:
                        st.success(f"Thank you, {student_row[3]}! Redirecting to a fun thank-you page...")
                        st.session_state.thank_you_name = student_row[3]
                        navigate_to('thank_you')
                    else:
                        st.error("Could not submit feedback. Please try again.")
    
    if st.button("← Back to Home"):
        navigate_to('home')
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_admin_dashboard():
    st.markdown('<h2>👨‍💼 Admin Dashboard</h2>', unsafe_allow_html=True)
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.admin_logged_in = False
        navigate_to('home')
    
    # Add new teacher section
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>➕ Add New Teacher</h3>', unsafe_allow_html=True)
    
    with st.form("add_teacher_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username")
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
        
        with col2:
            password = st.text_input("Password", type="password")
            subject = st.text_input("Subject")
        
        add_teacher = st.form_submit_button("Add Teacher")
        
        if add_teacher:
            if username and password and full_name and subject:
                if db.add_teacher(username, password, full_name, email, subject):
                    st.success("Teacher added successfully!")
                else:
                    st.error("Username already exists!")
            else:
                st.error("Please fill all required fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # View all teachers
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>👥 All Teachers</h3>', unsafe_allow_html=True)
    
    teachers = db.get_all_teachers()
    
    if teachers:
        for teacher in teachers:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{teacher[2]}** ({teacher[4]})")
                st.write(f"Username: {teacher[1]} | Email: {teacher[3]}")
                st.write(f"Added: {teacher[5]}")
            
            with col2:
                feedback_count = len(db.get_feedback_for_teacher(teacher[0]))
                st.write(f"📝 {feedback_count} feedback")
            
            with col3:
                if st.button(f"🗑️ Delete", key=f"delete_{teacher[0]}"):
                    if db.delete_teacher(teacher[0]):
                        st.success("Teacher deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Error deleting teacher!")
            
            st.divider()
    else:
        st.info("No teachers found. Add some teachers to get started!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_teacher_dashboard():
    if not st.session_state.current_teacher:
        navigate_to('home')
        return
    
    teacher = st.session_state.current_teacher
    st.markdown(f'<h2>👩‍🏫 Teacher Dashboard - {teacher[3]}</h2>', unsafe_allow_html=True)
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.teacher_logged_in = False
        st.session_state.current_teacher = None
        navigate_to('home')
    
    # Teacher info
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>👤 Teacher Information</h3>', unsafe_allow_html=True)
    st.write(f"**Name:** {teacher[3]}")
    st.write(f"**Subject:** {teacher[5]}")
    st.write(f"**Email:** {teacher[4]}")
    st.write(f"**Username:** {teacher[1]}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Manage Students section
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>👥 Manage Students</h3>', unsafe_allow_html=True)
    with st.form("add_student_form"):
        new_student_name = st.text_input("Student Name", placeholder="Full name")
        add_student_btn = st.form_submit_button("Add Student (Auto-ID)")
        if add_student_btn:
            if new_student_name.strip():
                ok, generated_id = db.add_student_auto(teacher[0], new_student_name.strip())
                if ok:
                    st.success(f"Student added. Generated ID: {generated_id}")
                else:
                    st.error("Could not add student. Please try again.")
            else:
                st.error("Please provide the Student Name.")

    # List existing students
    students = db.get_students_for_teacher(teacher[0])
    if students:
        for s in students:
            sid = s[2]
            sname = s[3]
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.write(f"{sname}")
            with c2:
                st.write(f"ID: {sid}")
            with c3:
                if st.button("🗑️ Remove", key=f"del_student_{sid}"):
                    if db.delete_student(teacher[0], sid):
                        st.success("Student removed.")
                        st.rerun()
                    else:
                        st.error("Could not remove student.")
    else:
        st.info("No students added yet.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Feedback section
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<h3>📝 Student Feedback</h3>', unsafe_allow_html=True)
    
    feedback_list = db.get_feedback_for_teacher(teacher[0])
    
    if feedback_list:
        for feedback in feedback_list:
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <strong>👤 {feedback[1]}</strong><br>
                <small>📅 {feedback[3]}</small><br><br>
                {feedback[2]}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No feedback received yet. Encourage your students to provide feedback!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_thank_you_page():
    name = st.session_state.get('thank_you_name', 'Student')
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown(f'<h2>🎉 Thank you, {name}!</h2>', unsafe_allow_html=True)
    st.write("You can play a quick mini-game below. Once done, you can close this page.")

    # Simple mini-game: number guess
    st.markdown('<h4>🎮 Mini Game: Guess the Number (1-10)</h4>', unsafe_allow_html=True)
    if 'game_number' not in st.session_state:
        import random
        st.session_state.game_number = random.randint(1, 10)
        st.session_state.game_over = False

    guess = st.number_input("Enter your guess", min_value=1, max_value=10, step=1)
    if st.button("Submit Guess") and not st.session_state.game_over:
        if guess == st.session_state.game_number:
            st.success("🎯 Correct! Great job! You can now close this page.")
            st.session_state.game_over = True
        elif guess < st.session_state.game_number:
            st.info("🔼 Try higher!")
        else:
            st.info("🔽 Try lower!")

    st.caption("Tip: Use the browser's close button or navigate away. You won't be able to return to the feedback form now.")

if __name__ == "__main__":
    main()
