# Blogify

Blogify is a Flask-based blogging platform with secure authentication, profile management, password recovery, post creation, comments, and a polished dark-themed interface.

## Features

- Secure registration and login flow with Flask-Bcrypt and Flask-WTF
- User profile updates and avatar uploads
- Password reset via Flask-Mail and temporary JWT tokens
- Full CRUD support for posts and comments
- Responsive layout with pagination and a modern UI

## Tech Stack

- Backend: Python 3, Flask, Flask-SQLAlchemy, Flask-Migrate
- Authentication and security: Flask-Login, Flask-Bcrypt, Flask-WTF, itsdangerous
- Mail: Flask-Mail
- Frontend: Jinja2 templates, HTML, CSS, and Bootstrap-style assets

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/prasenjitshinde27-byte/BLOGIFY.git
   cd BLOGIFY
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with:
   ```env
   SECRET_KEY=your_secret_key_here
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_email_app_password
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

6. Run the application:
   ```bash
   python fast.py
   ```

Open http://127.0.0.1:5000 in your browser.

## Project Structure

```text
BLOGIFY/
├── flaskblog/           # Main application package
├── instance/            # Local database and runtime files
├── migrations/          # Database migration history
├── fast.py              # Application entry point
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
