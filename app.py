"""
Production-Ready Portfolio Website - FIXED VERSION
Admin updates now show immediately on main page
Author: Dhananjay Kothawale
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3
import os
from datetime import datetime, timedelta
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Ensure required directories exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database connection
def get_db():
    """Get database connection"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Skills table
    c.execute('''CREATE TABLE IF NOT EXISTS skills
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category TEXT NOT NULL,
                  name TEXT NOT NULL,
                  order_num INTEGER DEFAULT 0)''')
    
    # Services table
    c.execute('''CREATE TABLE IF NOT EXISTS services
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT NOT NULL,
                  icon TEXT,
                  order_num INTEGER DEFAULT 0)''')
    
    # Projects table
    c.execute('''CREATE TABLE IF NOT EXISTS projects
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT NOT NULL,
                  tools TEXT,
                  results TEXT,
                  github_link TEXT,
                  linkedin_link TEXT,
                  image_path TEXT,
                  order_num INTEGER DEFAULT 0)''')
    
    # Experience table
    c.execute('''CREATE TABLE IF NOT EXISTS experience
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  organization TEXT NOT NULL,
                  role TEXT,
                  description TEXT NOT NULL,
                  certificate_path TEXT,
                  start_date TEXT,
                  end_date TEXT,
                  order_num INTEGER DEFAULT 0)''')
    
    # Certifications table
    c.execute('''CREATE TABLE IF NOT EXISTS certifications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  issuer TEXT,
                  date_earned TEXT,
                  order_num INTEGER DEFAULT 0)''')
    
    # Contact messages table
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  message TEXT NOT NULL,
                  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  is_read INTEGER DEFAULT 0)''')
    
    # Settings table
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (key TEXT PRIMARY KEY,
                  value TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()

# Seed initial data
def seed_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM skills")
    if c.fetchone()[0] == 0:
        skills_data = [
            ('Programming', 'Python', 1), ('Programming', 'SQL', 2),
            ('Programming', 'C', 3), ('Programming', 'C++', 4),
            ('Analytics', 'Pandas', 1), ('Analytics', 'NumPy', 2),
            ('Analytics', 'EDA', 3), ('Analytics', 'Statistics', 4),
            ('Visualization', 'Power BI', 1), ('Visualization', 'DAX', 2),
            ('Visualization', 'Excel', 3), ('Visualization', 'Matplotlib', 4),
            ('ML & AI', 'Scikit-learn', 1), ('ML & AI', 'OpenCV', 2),
            ('ML & AI', 'LLM Basics', 3), ('Backend', 'Flask', 1),
            ('Backend', 'REST APIs', 2), ('Backend', 'SQLite', 3),
            ('Backend', 'MySQL', 4), ('Tools', 'Git', 1),
            ('Tools', 'GitHub', 2), ('Tools', 'VS Code', 3), ('Tools', 'Jupyter', 4)
        ]
        c.executemany("INSERT INTO skills (category, name, order_num) VALUES (?, ?, ?)", skills_data)
        
        services_data = [
            ('Data Analysis & Insights', 'Transform raw data into actionable business insights through comprehensive analysis, statistical modeling, and data-driven recommendations that drive strategic decisions.', '📊', 1),
            ('Power BI Dashboard Development', 'Design and develop interactive, real-time dashboards that visualize complex data sets, track KPIs, and enable stakeholders to make informed decisions quickly.', '📈', 2),
            ('Business Intelligence Reporting', 'Create comprehensive BI reports with advanced analytics, trend analysis, and performance metrics to optimize business operations and identify growth opportunities.', '💼', 3),
            ('Predictive Analytics', 'Leverage machine learning algorithms and statistical models to forecast trends, predict outcomes, and provide data-backed projections for strategic planning.', '🔮', 4),
            ('Computer Vision Solutions', 'Develop intelligent systems using OpenCV and deep learning for facial recognition, object detection, and automated visual analysis applications.', '👁️', 5)
        ]
        c.executemany("INSERT INTO services (title, description, icon, order_num) VALUES (?, ?, ?, ?)", services_data)
        
        projects_data = [
            ('Face Recognition Attendance System', 'Developed an automated attendance system using advanced facial recognition technology. Implemented MTCNN for face detection and FaceNet for accurate face recognition, achieving 95% accuracy in real-world conditions.', 'MTCNN, FaceNet, OpenCV, Python, Deep Learning', '95% accuracy rate, 80% reduction in manual effort, Real-time processing capability', '', '', '', 1),
            ('Road Accident Analysis & Safety Insights', 'Comprehensive analysis of 144,000+ road accident records to identify high-risk zones, accident patterns, and temporal trends. Delivered actionable safety recommendations based on data-driven insights.', 'Python, Pandas, Power BI, Statistical Analysis, Geospatial Analysis', 'Analyzed 144,000+ records, Identified critical high-risk zones, Created predictive risk models, Delivered interactive dashboards', '', '', '', 2),
            ('Customer Analytics & Sales Forecasting', 'Built a comprehensive customer segmentation and sales forecasting system. Implemented machine learning models to predict sales trends and customer behavior, enabling data-driven marketing strategies.', 'Python, Scikit-learn, Pandas, Time Series Analysis, Clustering', '88% prediction accuracy, Customer segmentation across 5 distinct groups, Identified key revenue drivers, Optimized inventory planning', '', '', '', 3)
        ]
        c.executemany("INSERT INTO projects (title, description, tools, results, github_link, linkedin_link, image_path, order_num) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", projects_data)
        
        experience_data = [('296 Field Workshop Company, EME', 'Data Analytics Specialist', 'Delivered 10 advanced Power BI dashboards for defence operations, focusing on confidential data handling, decision-support analytics, and operational efficiency. Implemented strict data security protocols and provided actionable insights for mission-critical operations.', '', '', '', 1)]
        c.executemany("INSERT INTO experience (organization, role, description, certificate_path, start_date, end_date, order_num) VALUES (?, ?, ?, ?, ?, ?, ?)", experience_data)
        
        certifications_data = [
            ('Microsoft Career Essentials in Data Analysis', 'Microsoft', '2024', 1),
            ('Python Programming', 'CloudThat', '2024', 2),
            ('SQL for Data Analysis', 'Online Certification', '2024', 3),
            ('Power BI Data Visualization', 'Microsoft', '2024', 4),
            ('TECHNOYASH-25 - 1st Prize', 'Technical Competition', '2025', 5)
        ]
        c.executemany("INSERT INTO certifications (title, issuer, date_earned, order_num) VALUES (?, ?, ?, ?)", certifications_data)
        
        settings_data = [
            ('profile_name', 'Dhananjay Kothawale'),
            ('profile_title', 'Data Analyst | Power BI | Python | SQL | Machine Learning'),
            ('profile_location', 'Chhatrapati Sambhajinagar, Maharashtra, India'),
            ('profile_email', 'dhananjaykothawale80@gmail.com'),
            ('profile_linkedin', 'https://www.linkedin.com/in/dhananjay-kothawale/'),
            ('profile_summary', 'Data Science undergraduate (UG\'26) with a strong foundation in data analysis, visualization, and machine learning. Proven experience delivering defence-oriented Power BI dashboards with focus on KPIs, decision-support systems, and data integrity. Passionate about transforming complex data into actionable business insights.'),
            ('resume_path', 'uploads/resume.pdf'),
            ('profile_image', 'uploads/profile.jpg')
        ]
        c.executemany("INSERT INTO settings (key, value) VALUES (?, ?)", settings_data)
    
    conn.commit()
    conn.close()

init_db()
seed_data()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Helper function - NO CACHING
def get_setting(key, default=''):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = ?", (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else default

# CRITICAL: Prevent browser caching of dynamic pages
@app.after_request
def add_no_cache(response):
    """Prevent caching of dynamic content"""
    if request.endpoint and 'static' not in request.endpoint:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
    return response

# Health check for keep-alive services
@app.route('/health')
def health_check():
    return {'status': 'ok', 'timestamp': datetime.now().isoformat()}, 200

# Main route - Always fresh data
@app.route('/')
def index():
    conn = get_db()
    c = conn.cursor()
    
    # Fetch fresh data from database
    c.execute("SELECT * FROM skills ORDER BY category, order_num")
    skills = c.fetchall()
    
    c.execute("SELECT * FROM services ORDER BY order_num")
    services = c.fetchall()
    
    c.execute("SELECT * FROM projects ORDER BY order_num")
    projects = c.fetchall()
    
    c.execute("SELECT * FROM experience ORDER BY order_num")
    experience = c.fetchall()
    
    c.execute("SELECT * FROM certifications ORDER BY order_num")
    certifications = c.fetchall()
    
    conn.close()
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        category = skill['category']
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill['name'])
    
    # Get profile settings - fresh every time
    profile = {
        'name': get_setting('profile_name'),
        'title': get_setting('profile_title'),
        'location': get_setting('profile_location'),
        'email': get_setting('profile_email'),
        'linkedin': get_setting('profile_linkedin'),
        'summary': get_setting('profile_summary'),
        'image': get_setting('profile_image')
    }
    
    return render_template('index.html',
                         profile=profile,
                         skills=skills_by_category,
                         services=services,
                         projects=projects,
                         experience=experience,
                         certifications=certifications)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()
    
    if not name or not email or not message:
        flash('All fields are required.', 'error')
        return redirect(url_for('index') + '#contact')
    
    if '@' not in email or '.' not in email:
        flash('Please enter a valid email address.', 'error')
        return redirect(url_for('index') + '#contact')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()
    
    flash('Thank you for your message! I will get back to you soon.', 'success')
    return redirect(url_for('index') + '#contact')

@app.route('/download-resume')
def download_resume():
    resume_path = get_setting('resume_path', 'uploads/resume.pdf')
    if os.path.exists(resume_path):
        return send_file(resume_path, as_attachment=True, download_name='Dhananjay_Kothawale_Resume.pdf')
    flash('Resume file not found.', 'error')
    return redirect(url_for('index'))

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == app.config['ADMIN_USERNAME'] and check_password_hash(app.config['ADMIN_PASSWORD'], password):
            session['admin_logged_in'] = True
            session.permanent = True
            app.permanent_session_lifetime = timedelta(hours=24)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials.', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT * FROM skills ORDER BY category, order_num")
    skills = c.fetchall()
    c.execute("SELECT * FROM services ORDER BY order_num")
    services = c.fetchall()
    c.execute("SELECT * FROM projects ORDER BY order_num")
    projects = c.fetchall()
    c.execute("SELECT * FROM experience ORDER BY order_num")
    experience = c.fetchall()
    c.execute("SELECT * FROM certifications ORDER BY order_num")
    certifications = c.fetchall()
    c.execute("SELECT * FROM messages ORDER BY submitted_at DESC LIMIT 50")
    messages = c.fetchall()
    c.execute("SELECT * FROM settings")
    settings_rows = c.fetchall()
    settings = {row['key']: row['value'] for row in settings_rows}
    
    conn.close()
    
    return render_template('admin_dashboard.html',
                         skills=skills, services=services, projects=projects,
                         experience=experience, certifications=certifications,
                         messages=messages, settings=settings)

# Skills CRUD
@app.route('/admin/skills/add', methods=['POST'])
@login_required
def add_skill():
    category = request.form.get('category')
    name = request.form.get('name')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO skills (category, name) VALUES (?, ?)", (category, name))
    conn.commit()
    conn.close()
    
    flash('Skill added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/skills/edit/<int:skill_id>', methods=['POST'])
@login_required
def edit_skill(skill_id):
    category = request.form.get('category')
    name = request.form.get('name')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE skills SET category = ?, name = ? WHERE id = ?", (category, name, skill_id))
    conn.commit()
    conn.close()
    
    flash('Skill updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/skills/delete/<int:skill_id>')
@login_required
def delete_skill(skill_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM skills WHERE id = ?", (skill_id,))
    conn.commit()
    conn.close()
    
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Services CRUD
@app.route('/admin/services/add', methods=['POST'])
@login_required
def add_service():
    title = request.form.get('title')
    description = request.form.get('description')
    icon = request.form.get('icon')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO services (title, description, icon) VALUES (?, ?, ?)", (title, description, icon))
    conn.commit()
    conn.close()
    
    flash('Service added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/services/edit/<int:service_id>', methods=['POST'])
@login_required
def edit_service(service_id):
    title = request.form.get('title')
    description = request.form.get('description')
    icon = request.form.get('icon')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE services SET title = ?, description = ?, icon = ? WHERE id = ?", 
              (title, description, icon, service_id))
    conn.commit()
    conn.close()
    
    flash('Service updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/services/delete/<int:service_id>')
@login_required
def delete_service(service_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM services WHERE id = ?", (service_id,))
    conn.commit()
    conn.close()
    
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Projects CRUD
@app.route('/admin/projects/add', methods=['POST'])
@login_required
def add_project():
    title = request.form.get('title')
    description = request.form.get('description')
    tools = request.form.get('tools')
    results = request.form.get('results')
    github_link = request.form.get('github_link')
    linkedin_link = request.form.get('linkedin_link')
    
    image_path = ''
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            image_path = filepath
    
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO projects (title, description, tools, results, github_link, linkedin_link, image_path) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
             (title, description, tools, results, github_link, linkedin_link, image_path))
    conn.commit()
    conn.close()
    
    flash('Project added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/projects/edit/<int:project_id>', methods=['POST'])
@login_required
def edit_project(project_id):
    title = request.form.get('title')
    description = request.form.get('description')
    tools = request.form.get('tools')
    results = request.form.get('results')
    github_link = request.form.get('github_link')
    linkedin_link = request.form.get('linkedin_link')
    
    image_path = request.form.get('existing_image', '')
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            image_path = filepath
    
    conn = get_db()
    c = conn.cursor()
    c.execute("""UPDATE projects SET title = ?, description = ?, tools = ?, results = ?, 
                 github_link = ?, linkedin_link = ?, image_path = ? WHERE id = ?""",
             (title, description, tools, results, github_link, linkedin_link, image_path, project_id))
    conn.commit()
    conn.close()
    
    flash('Project updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/projects/delete/<int:project_id>')
@login_required
def delete_project(project_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Certifications CRUD
@app.route('/admin/certifications/add', methods=['POST'])
@login_required
def add_certification():
    title = request.form.get('title')
    issuer = request.form.get('issuer')
    date_earned = request.form.get('date_earned')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO certifications (title, issuer, date_earned) VALUES (?, ?, ?)", 
              (title, issuer, date_earned))
    conn.commit()
    conn.close()
    
    flash('Certification added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/certifications/edit/<int:cert_id>', methods=['POST'])
@login_required
def edit_certification(cert_id):
    title = request.form.get('title')
    issuer = request.form.get('issuer')
    date_earned = request.form.get('date_earned')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE certifications SET title = ?, issuer = ?, date_earned = ? WHERE id = ?", 
              (title, issuer, date_earned, cert_id))
    conn.commit()
    conn.close()
    
    flash('Certification updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/certifications/delete/<int:cert_id>')
@login_required
def delete_certification(cert_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM certifications WHERE id = ?", (cert_id,))
    conn.commit()
    conn.close()
    
    flash('Certification deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Settings update
@app.route('/admin/settings/update', methods=['POST'])
@login_required
def update_settings():
    conn = get_db()
    c = conn.cursor()
    
    # Update text settings
    for key in ['profile_name', 'profile_title', 'profile_location', 'profile_email', 'profile_linkedin', 'profile_summary']:
        value = request.form.get(key)
        if value:
            c.execute("UPDATE settings SET value = ? WHERE key = ?", (value, key))
    
    # Handle profile image upload
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and file.filename and allowed_file(file.filename):
            filename = 'profile.' + file.filename.rsplit('.', 1)[1].lower()
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            c.execute("UPDATE settings SET value = ? WHERE key = 'profile_image'", (filepath,))
    
    # Handle resume upload
    if 'resume' in request.files:
        file = request.files['resume']
        if file and file.filename and allowed_file(file.filename):
            filename = 'resume.pdf'
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            c.execute("UPDATE settings SET value = ? WHERE key = 'resume_path'", (filepath,))
    
    conn.commit()
    conn.close()
    
    flash('Settings updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)