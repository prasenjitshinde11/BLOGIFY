# 📝 Blogify — Modern content sharing platform

Blogify is a robust, full-featured content management and blogging web application built with Python and Flask. Recently modernized with a premium glassmorphic dark-theme UI, optimized database structures, and repaired core workflows, Blogify offers a distraction-free writing and reading environment.

---

## ✨ Features

- **🔒 Advanced Authentication:** Secure registration and login workflows using password hashing (Bcrypt), complete with a modern split-screen interface and brand storytelling panel.
- **🎨 Glassmorphism Dark UI:** Exquisite dark mode interface styled with customized vanilla CSS, fluid CSS variables, Google Fonts (Inter), and high-quality Tabler Icons.
- **📝 CRUD Operations:** Create, edit, and delete articles with custom title and body.
- **💬 Real-time Comments:** Read and write comments on posts immediately under articles.
- **⚙️ User Profile Management:** Change account username, email, and upload profile pictures with dynamic caching bust.
- **🔑 Password Recovery:** Secure email-based reset system powered by temporary JSON Web Tokens (JWT) and Flask-Mail.
- **🔍 Advanced Layout & Discovery:** Responsive mobile navigation, search bar integration, pagination, and a trending topics/categories sidebar.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask (Blueprints, Flask-Login, Flask-Mail)
- **Security:** Flask-Bcrypt, Flask-WTF (CSRF Protection), Itsdangerous (JWT Token generation)
- **Database:** SQLite / SQLAlchemy, Flask-Migrate (Alembic)
- **Frontend:** HTML5, Modern CSS (Glassmorphism), Jinja2 Templating, Tabler Icons

---

## 📸 Redesigned Interface

Here is a glimpse of the new premium dark-themed user experience:

### 🔑 Split-Screen Authentication Page
*Featuring high-impact statistics, brand testimonials, and a sleek login/registration form.*

![Auth Screen Preview](flaskblog/static/profile_pics/default.jpg) <!-- Replace or add a screenshot reference here -->

---

## 🚀 Getting Started

### 📋 Prerequisites

Make sure you have Python 3.10+ installed on your machine.

### ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/prasenjitshinde27-byte/BLOGIFY.git
   cd BLOGIFY
   ```

2. **Set up Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add:
   ```env
   SECRET_KEY=your_super_secret_key_here
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_email_app_password
   ```

5. **Initialize Database:**
   ```bash
   flask db upgrade
   ```

6. **Run the Application:**
   ```bash
   python fast.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## ⚙️ Project Structure

```
BLOGIFY/
│
├── flaskblog/               # Core application package
│   ├── errors/              # Error blueprint handlers
│   ├── main/                # Main site navigation blueprint
│   ├── posts/               # Article & CRUD logic blueprint
│   ├── users/               # Authentication, user profile & mail blueprint
│   ├── templates/           # Jinja2 template files
│   ├── static/              # CSS stylesheets and user uploads
│   ├── __init__.py          # App initialization & factory pattern
│   ├── config.py            # App configurations
│   └── models.py            # Database tables schema (User, Post, Comment)
│
├── instance/                # Local database file storage
├── migrations/              # Database migration history
├── .env                     # App environment configuration secrets (ignored)
├── .gitignore               # Ignored files list
├── requirements.txt         # Project dependencies list
└── fast.py                  # Application entry runner point
```
