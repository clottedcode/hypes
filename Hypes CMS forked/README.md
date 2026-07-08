# Hypes CMS — Python Flask Content Management System

Hypes CMS is a **forked** professional-grade, fully functional dynamic web application developed as an MVC showcase model. Built using Python Flask, Jinja2, SQLite with SQLAlchemy ORM, and Bootstrap 5, the application is designed to meet final year college project specifications, showcasing state-of-the-art software engineering best practices.

## Add-ons

- Aero Button Style

- Full sized hero images

## Support and help

For support write me at ronanbakker95@gmail.com

---

## Key Features

### Secure User Authentication & Management

* **Role-Based Access Control**: Clean division between general users and administrators.
* ** Werkzeug Cryptography**: Robust, secure password hashing using PBKDF2 with SHA256.
* **Session Management**: Persistent sessions and "Remember Me" features via Flask-Login.
* **Custom Profile Management**: Users can update emails, custom usernames, and upload unique profile images.

### Administrative Dashboard & Analytics

* **Overview Analytics Cards**: Dynamic count grids mapping total posts, comments, categories, and users.
* **Graphing Integrations**: Premium doughnut charts illustrating posts density across categories dynamically using **Chart.js** via CDN.
* **Category Post Status Metrics**: Progress bars tracking draft vs. published articles ratio.
* **Activity Lists**: Quick tables summarizing recent user signups and articles published.

### Full CRUD & Content Controls

* **Articles Management Table**: Admin overview for managing blog posts.
* **Dynamic Article Forms**: Form validation mapping WTForms. Includes **CKEditor 5** rich text editor CDN for an elegant posting experience.
* **Dynamic Categories**: Admin CRUD interface to map and manage categorizations.
* **SEO-Friendly URL Slugs**: Auto-generating unique, URL-safe post slugs to prevent path collisions.

### Rich User Engagements & UX

* **AJAX Commenting Thread**: Live, dynamic comment submissions and updates without full page reloads, using native Javascript fetch API.
* **Dynamic Keyword Search**: Filter articles globally across titles and contents.
* **Dynamic Sidebar Categorizations**: Multi-page sidebar categorization counts mapping published items.
* **Modular Theme Toggling**: Seamless **Dark and Light mode** toggle with local storage preference persistence.

---

## Architecture Design (MVC Structure)

The project cleanly implements the Model-View-Controller pattern:

```text
D:\CMS project/
├── requirements.txt         # Project package dependencies
├── README.md                # Development guide documentation
├── run.py                   # App Factory entrypoint and SQLite seeder
├── config.py                # Server, database, and upload configurations
├── models/                  # [Models] Database declarations & SQLAlchemy classes
│   ├── __init__.py          # Exposed collective namespace exports
│   ├── user.py              # User profiles logic and password hashes
│   ├── post.py              # Article schema, draft controls, unique slug creator
│   ├── category.py          # Category labels and post relationships
│   └── comment.py           # Comment posts mapping user & article targets
├── forms/                   # [Forms] Flask-WTF input validation
│   ├── __init__.py
│   ├── auth.py              # User logins, signups and profile changes
│   ├── post.py              # Article creations and cover validations
│   └── category.py          # Category creation and modifications
├── routes/                  # [Controllers] Flask Blueprints and endpoint routes
│   ├── __init__.py          # Consolidated blueprint exports
│   ├── auth.py              # Auth controls (Login, register, profile)
│   ├── main.py              # Public screens (Home, search, comment AJAX handlers)
│   ├── admin.py             # Administrative controls and CRUDs
│   └── utils.py             # Upload directories creations and image handlers
├── static/                  # [Views - Assets] Static layout resources
│   ├── css/
│   │   └── style.css        # Premium dark/light themes and custom elevations
│   ├── js/
│   │   └── main.js          # Theme persistence, AJAX comments, and Chart.js graphs
│   └── uploads/             # Server images storage (profiles & posts covers)
└── templates/               # [Views - Markup] Modular Jinja2 layouts
    ├── base.html            # Global navbar, dark-mode togglers and footer layout
    ├── index.html           # Homepage listing published posts and sidebars
    ├── post_detail.html     # Single post details and dynamic comments engine
    ├── search.html          # Dynamic search hits listing
    ├── profile.html         # Profile settings updates
    ├── about.html           # Academic abstract and technology stacks details
    ├── contact.html         # Interactive message box
    ├── errors/              # Custom HTML exception handlers (404 / 500)
    └── dashboard/           # Admin panel layouts
        ├── base.html        # Control panel sidebar layouts
        ├── index.html       # Analytics overview graphics and counters
        ├── posts.html       # Post lists CRUD panel
        ├── categories.html  # Categories list CRUD panel
        ├── users.html       # Dynamic users overview
        ├── post_form.html   # Rich-editor articles forms (CKEditor 5)
        └── category_form.html # Categories creation forms
```

---

## Step-by-Step Local Setup

Follow these straightforward commands in your terminal to initialize and run the project:

### 1. Clone or Move to Project Folder

Navigate to the directory in your system:

```bash
cd "D:\CMS project"
```

### 2. Configure Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies locally:

```bash
# Create the environment
python -m venv venv

# Activate on Windows (Command Prompt / Powershell)
.\venv\Scripts\activate
```

### 3. Install Required Packages

Install Flask and its extensions using the requirements file:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Start the development server:

```bash
python run.py
```

* The server will boot locally at: **`http://127.0.0.1:5000`**
* Upon startup, SQLite database tables are created automatically (`cms.db`).

---

## Seeded Administrator Credentials

To facilitate rapid testing, the system automatically detects empty databases and injects default categories along with an administrative account. 

Use the following credentials to access the secured **Admin Dashboard**:

* **Admin Login Email**: `admin@cms.com`
* **Admin Password**: `admin123`

---

## Tech Stack Summary

* **Language**: Python 3
* **Framework**: Flask 3
* **Forms Manager**: Flask-WTF & WTForms
* **ORM Engine**: SQLAlchemy (SQLite Database)
* **Frontend**: Jinja2 Template Engine & Bootstrap 5.3
* **Asset Libs**: Bootstrap Icons, Animate.css, Chart.js, CKEditor 5
