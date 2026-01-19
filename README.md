# 🚀 Professional Data Analyst Portfolio

A production-ready, recruiter-grade portfolio website built with Flask, featuring secure admin panel, dynamic content management, and premium dark theme UI.

## ✨ Features

- **Recruiter-Grade Design**: Premium dark theme (navy/charcoal) with smooth animations
- **Secure Admin Panel**: Session-based authentication with environment variable credentials
- **Dynamic Content Management**: Full CRUD operations for all sections
- **Functional Contact System**: Real contact form with database storage
- **One-Click Resume Download**: Direct PDF download functionality
- **Fully Responsive**: Mobile-first design that works on all devices
- **Production Ready**: Optimized for deployment on Render, Railway, or similar platforms

## 📁 Project Structure

```
portfolio/
├── app.py                      # Main Flask application
├── config.py                   # Configuration (uses ENV variables)
├── database.db                 # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
├── uploads/                    # Image and file uploads
│   ├── profile.jpg            # Profile photo
│   ├── resume.pdf             # Resume file
│   └── ...                    # Other uploads
├── templates/
│   ├── index.html             # Main portfolio page
│   ├── admin_login.html       # Admin login page
│   └── admin_dashboard.html   # Admin dashboard
└── static/
    ├── style.css              # Premium dark theme styles
    └── script.js              # Interactive features
```

## 🔧 Installation & Setup

### 1. Clone or Download Project

```bash
# Navigate to project directory
cd portfolio
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

**For Development (Local Testing):**

Create a `.env` file or set environment variables:

```bash
# Windows (Command Prompt)
set SECRET_KEY=your-super-secret-key-change-this
set ADMIN_USERNAME=admin
set ADMIN_PASSWORD=your-strong-password

# Mac/Linux
export SECRET_KEY=your-super-secret-key-change-this
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=your-strong-password
```

**For Production (Render/Railway):**

Set these as environment variables in your deployment platform:
- `SECRET_KEY`: A random, secure string (generate using `python -c "import secrets; print(secrets.token_hex(32))"`)
- `ADMIN_USERNAME`: Your admin username
- `ADMIN_PASSWORD`: Your admin password (will be hashed automatically)

### 5. Prepare Upload Files

Create the `uploads` folder and add your files:

```bash
mkdir uploads
```

Add these files to the `uploads` folder:
- `resume.pdf` - Your resume
- `profile.jpg` - Your profile photo (optional)
- Any project images or certificates

### 6. Run the Application

```bash
python app.py
```

The application will:
- Automatically create the SQLite database
- Initialize with seed data
- Start the server at `http://localhost:5000`

## 🔐 Admin Access

1. Navigate to: `http://localhost:5000/admin/login`
2. Login with your credentials (set via environment variables)
3. Access the admin dashboard to manage all content

**Default credentials (CHANGE IMMEDIATELY):**
- Username: `admin`
- Password: `admin123`

## 📊 Admin Panel Features

The admin dashboard allows you to:

- ✏️ **Update Profile**: Name, title, email, location, summary
- 📄 **Upload Resume**: Replace resume PDF file
- 🛠️ **Manage Skills**: Add/delete skills by category
- 💼 **Manage Projects**: Add/edit/delete projects with images
- 📧 **View Messages**: Read contact form submissions
- ⚙️ **Update Settings**: Modify all profile information

## 🚀 Deployment

### Deploy to Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**: Add `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`
4. Deploy!


```

## 📝 Content Management

### Adding Skills

1. Login to admin panel
2. Navigate to "Skills Management"
3. Enter category and skill name
4. Click "Add Skill"

### Adding Projects

1. Login to admin panel
2. Navigate to "Projects Management"
3. Fill in project details:
   - Title, description, tools, results
   - GitHub/LinkedIn links
   - Upload project image
4. Click "Add Project"

### Updating Profile

1. Login to admin panel
2. Navigate to "Profile Settings"
3. Update any field
4. Upload new resume if needed
5. Click "Update Profile"

## 🎨 Customization

### Colors

Edit `static/style.css` CSS variables:

```css
:root {
    --navy-dark: #0a192f;
    --navy-light: #112240;
    --accent: #64ffda;
    /* ... */
}
```

### Typography

Change fonts in `templates/index.html` and CSS:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

## 🔒 Security Best Practices

- ✅ Never commit `.env` file or credentials to Git
- ✅ Use strong, unique passwords for admin access
- ✅ Generate a random SECRET_KEY for production
- ✅ Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- ✅ Use HTTPS in production (Render/Railway provide this automatically)

## 📧 Contact Form

The contact form:
- ✅ Validates all inputs (frontend + backend)
- ✅ Stores messages in SQLite database
- ✅ Shows success/error feedback
- ✅ Admin can view all messages in dashboard

## 🐛 Troubleshooting

### Database Issues

If database gets corrupted:
```bash
rm database.db
python app.py  # Will recreate and seed data
```

### File Upload Issues

Ensure `uploads` folder exists and has write permissions:
```bash
mkdir uploads
chmod 755 uploads
```

### Environment Variables Not Working

Verify they're set correctly:
```python
python -c "import os; print(os.environ.get('ADMIN_USERNAME'))"
```

## 📄 License

This is a personal portfolio project. Feel free to use as a template for your own portfolio.

## 🙋 Support

For issues or questions:
- Check the code comments
- Review Flask documentation
- Ensure all environment variables are set correctly
- Verify file paths and permissions

---
🚀 To Deploy Changes to Render
After testing locally:
Step 1: Commit Changes


**git add .
git commit -m "Updated portfolio content
git push**


**Built with ❤️ using Flask, Python, and modern web technologies**