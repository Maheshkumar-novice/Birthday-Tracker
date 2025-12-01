# 🎂 Birthday Tracker

A simple, elegant web application for tracking birthdays built with Flask.

## Features

- ✨ Clean, professional UI
- 📅 Track birthdays with names, dates, categories, and notes
- 🏷️ Organize by categories (Family, Friends, Work, Other)
- 📊 Table view with automatic sorting by upcoming birthdays
- 🔐 Simple password protection
- 📱 Mobile-friendly responsive design
- 💾 SQLite database

## Quick Start

### Prerequisites

- Python 3.13+
- uv (recommended) or pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd birthdays
```

2. Install dependencies:
```bash
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
```

### Running the App

```bash
uv run python run.py
```

Or:
```bash
python run.py
```

Visit `http://127.0.0.1:5000` in your browser.

**Default password:** `birthday123`

## Configuration

Edit `config.py` to customize:

- `SECRET_KEY`: Session encryption key (change in production!)
- `APP_PASSWORD`: Login password (default: `birthday123`)
- `SQLALCHEMY_DATABASE_URI`: Database location

For production, use environment variables:
```bash
export SECRET_KEY="your-secret-key"
export APP_PASSWORD="your-password"
```

## Project Structure

```
birthdays/
├── app/
│   ├── static/
│   │   ├── css/          # Modular stylesheets
│   │   └── app.js        # Client-side JavaScript
│   ├── templates/        # Jinja2 templates
│   ├── __init__.py       # App factory
│   ├── auth.py          # Authentication
│   ├── models.py        # Database models
│   └── routes.py        # Application routes
├── config.py            # Configuration
├── run.py              # Application entry point
└── birthdays.db        # SQLite database (auto-created)
```

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy
- **Frontend:** HTML5, CSS3 (modular), Vanilla JavaScript
- **Database:** SQLite
- **Authentication:** Flask sessions with simple password protection

## Security Notes

⚠️ **Important for production:**

1. Change `SECRET_KEY` and `APP_PASSWORD` in `config.py`
2. Use environment variables for sensitive data
3. Use HTTPS in production
4. Consider more robust auth for public deployment

## License

MIT License - Feel free to use and modify!

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
