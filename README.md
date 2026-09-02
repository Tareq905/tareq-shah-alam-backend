# 🌌 Md Tareq Shah Alam — Portfolio Backend & Admin API

This is the production-ready **Django REST API** and **Jazzmin Admin Control Center** powering **Md Tareq Shah Alam's Machine Learning & Data Science Portfolio**.

---

## 🏗️ Architecture & Features

- **Framework**: Django 6.x + Django REST Framework (DRF)
- **Admin UI**: Customized Dark Cyberpunk `Jazzmin` Theme (Purple & Cyan neon accents)
- **Database**: 
  - **Local Development**: SQLite (Automatic fallback)
  - **Production Deployment**: PostgreSQL via `DATABASE_URL` / `dj-database-url`
- **Security & AI Gatekeeper**:
  - **Anti-Tempmail Filter**: Rejects 1,000+ disposable email domains (`@tempmail.com`, `@mailinator.com`, etc.).
  - **Bot & Keyboard-Mash Filter**: Intercepts random keystrokes (e.g. `ahaadf@gmail.com`, `asdf123@...`) and fake names (`lijo`, `asdfgh`, `test user`).
  - **Deep Groq AI Validation**: Uses Groq LLM inference (`openai/gpt-oss-120b`, `qwen3.8-27b`) to verify sender legitimacy before saving inquiries.

---

## 📁 Apps Structure

```
backend/
├── core/                  # Singleton Site Settings (Name, Bio, WhatsApp, Medium/Blog, Socials)
│   ├── models.py
│   ├── admin.py
│   ├── serializers.py
│   └── views.py
├── portfolio/             # Dynamic Portfolio Components
│   ├── models.py          # Education, Experience (Reverse Chronological), Projects, Research Papers
│   ├── admin.py
│   ├── serializers.py
│   └── views.py
├── contacts/              # Inquiry Management & AI Anti-Spam Gatekeeper
│   ├── models.py          # ContactMessage with AI Badges
│   ├── validators.py      # Heuristic & Groq LLM Authenticity Validator
│   ├── serializers.py
│   └── views.py
├── portfolio_backend/     # Main Settings, WSGI & URL Routing
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── seed_data.py           # Initial data & superuser seed script
```

---

## ⚡ Local Setup & Run

### 1. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables (`.env`)
Create a `.env` file in the `backend/` directory:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,.pythonanywhere.com
GROQ_API_KEY=gsk_your_groq_api_key_here

# Optional: PostgreSQL Database URL (Leave empty for SQLite local default)
# DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

### 4. Run Migrations & Seed Real Data
```bash
python manage.py makemigrations core portfolio contacts
python manage.py migrate
python seed_data.py
```

### 5. Start Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Consolidated API**: [http://127.0.0.1:8000/api/all/](http://127.0.0.1:8000/api/all/)

---

## 🌐 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/site-settings/` | Returns full name, bio, WhatsApp phone number, Blog/Medium URL, and social links. |
| `GET` | `/api/education/` | Returns academic qualifications (B.Sc., M.Sc., CGPA, Thesis description). |
| `GET` | `/api/experience/` | Returns work experiences ordered chronologically (Present on top). |
| `GET` | `/api/projects/` | Returns active applied AI/ML projects with live demo & GitHub repository URLs. |
| `GET` | `/api/research/` | Returns research papers, preprints, publication venue, and PDF links. |
| `GET` | `/api/all/` | **High-speed single bundle** returning all portfolio data in 1 fast query. |
| `POST` | `/api/contact/` | Submits inquiry, runs AI & tempmail filters, and saves verified inquiries to DB. |

---

## 🚀 PythonAnywhere Deployment Step-by-Step

### 1. Upload or Clone Repository
In PythonAnywhere **Bash Console**:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo/backend
```

### 2. Create Virtualenv & Install Requirements
```bash
mkvirtualenv --python=/usr/bin/python3.10 myportfolio-venv
pip install -r requirements.txt
```

### 3. Configure Database & Static Files
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 4. Configure Web Tab on PythonAnywhere
- **Virtualenv**: `/home/yourusername/.virtualenvs/myportfolio-venv`
- **Source code**: `/home/yourusername/your-repo/backend`
- **Working directory**: `/home/yourusername/your-repo/backend`
- **Static files mapping**:
  - URL: `/static/` ➔ Directory: `/home/yourusername/your-repo/backend/staticfiles`
  - URL: `/media/` ➔ Directory: `/home/yourusername/your-repo/backend/media`

### 5. Configure WSGI Configuration File (`/var/www/..._wsgi.py`)
Replace contents with:
```python
import os
import sys
from dotenv import load_dotenv

path = '/home/yourusername/your-repo/backend'
if path not in sys.path:
    sys.path.append(path)

load_dotenv(os.path.join(path, '.env'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'portfolio_backend.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 6. Reload Web App
Click **Reload** in PythonAnywhere Web Tab. Your backend is live at:
👉 `https://yourusername.pythonanywhere.com/admin/`

---

## 🛡️ License & Credits
Developed with ❤️ by **Md Tareq Shah Alam** • 2026
