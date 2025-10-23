# Wedding Guest List Application

A Flask-based web application for managing wedding guest lists with multiple user support.

## Features

- 🔐 Multi-user authentication (5 users by default)
- 📊 Real-time statistics (total guests, likely attendees, groom/bride side breakdown)
- ➕ Add, edit, and delete guests
- 📱 Responsive design
- 🎨 Modern, elegant UI
- 💾 SQLite database for data persistence

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python init_db.py
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Default Users

You can log in with any of these credentials:

- **Username:** sarah | **Password:** password123
- **Username:** john | **Password:** password123
- **Username:** emma | **Password:** password123
- **Username:** michael | **Password:** password123
- **Username:** admin | **Password:** admin123

## Configuration

### Adding/Modifying Users

Edit the `config.py` file to add or modify users:

```python
USERS = {
    'username': 'password',
    'another_user': 'another_password'
}
```

### Changing App Settings

In `config.py`, you can modify:

- `SECRET_KEY` - Flask session secret (change in production!)
- `DATABASE_PATH` - Location of the SQLite database
- `APP_TITLE` - Application title displayed in the UI
- `DEBUG_MODE` - Enable/disable debug mode

## Project Structure

```
wedding-list-app/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── init_db.py             # Database initialization script
├── models/
│   └── database.py        # Database models and operations
├── templates/
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   └── dashboard.html     # Main dashboard
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheets
│   └── js/
│       └── main.js        # JavaScript
└── data/
    └── wedding_list.db    # SQLite database (created automatically)
```

## Guest Fields

Each guest entry contains:

- **Name** - Guest or family name
- **Count** - Number of people in the party
- **Side** - Groom's side or Bride's side
- **Attendance** - Likely or Unlikely to attend

## Security Notes

⚠️ **Important for Production:**

1. Change the `SECRET_KEY` in `config.py`
2. Use hashed passwords instead of plain text
3. Enable HTTPS
4. Set `DEBUG_MODE = False`
5. Use a production WSGI server (gunicorn, uwsgi)

## Troubleshooting

**Database not found?**
- Run `python init_db.py` to create the database

**Can't log in?**
- Check your credentials in `config.py`
- Ensure you're using the correct username/password

**Port already in use?**
- Change the port in `app.py`: `app.run(port=5001)`

## License

Free to use for personal projects.