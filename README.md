# Legal Laboratory - Django Web Platform

A comprehensive legal education and gamified learning platform built with Django.

## Features

- **User Management**: Registration, authentication, and profiles with different account types (Student, Professional, Lecturer)
- **Legal Education**: Structured educational content with categories, articles, and exam materials
- **Gamified Learning**: Interactive legal games including:
  - Courtroom Simulations
  - Criminal Case Analysis
  - Legal Tests & Quizzes
  - Correct/Incorrect Scenarios
- **Case Laboratory**: Practical case analysis and evaluation
- **Chat & Consultation**: Online chat with lawyers and consultation scheduling
- **News & Blog**: Legal news, legislative updates, and analytical articles
- **Leaderboard**: Ranking system for gamified learning
- **Full Admin Panel**: All content manageable via Django Admin

## Installation

1. **Clone the repository**
   ```bash
   cd Loyer_
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Project Structure

```
legal_lab/
├── accounts/          # User authentication and profiles
├── core/              # Home, About, Contact pages
├── education/         # Legal education content
├── games/            # Gamified learning system
├── cases/            # Case laboratory
├── chat/             # Chat and consultation
├── news/             # News and blog
├── templates/        # HTML templates
├── static/           # Static files (CSS, JS, images)
├── media/            # User uploaded files
└── legal_lab/       # Project settings
```

## Admin Panel Setup

All content is managed through the Django Admin Panel. After creating a superuser, you can:

1. **Add Slider Items**: Home page carousel content
2. **Manage Education Categories**: Create legal education sections
3. **Create Games**: Set up game scenarios, questions, and answers
4. **Add Legal Cases**: Create cases for the case laboratory
5. **Manage News**: Publish news articles and blog posts
6. **Configure Contact Info**: Update contact information
7. **View Messages**: Monitor contact form submissions and chat messages

## Key Models

- **User**: Custom user model with account types and points system
- **Game**: Game instances with questions and scoring
- **LegalCase**: Cases for analysis and evaluation
- **Article**: Educational articles and news
- **ChatRoom**: Chat rooms for consultations
- **Leaderboard**: User rankings and statistics

## Design

- **Color Theme**: Blue (primary: #1e3a8a)
- **Responsive**: Fully responsive design for desktop, tablet, and mobile
- **Modern UI**: Clean, professional interface with smooth animations
- **No External Libraries**: Pure CSS and JavaScript (except Django)

## Development

### Creating Content via Admin

1. Login to admin panel
2. Navigate to the relevant section
3. Add/edit content as needed
4. All changes are immediately reflected on the website

### Adding New Game Types

1. Go to Games > Game Types in admin
2. Add a new game type with icon and description
3. Create games under that type
4. Add questions and answers for each game

### Managing Educational Content

1. Go to Education > Education Categories
2. Create categories (Criminal Law, Civil Law, etc.)
3. Add articles and exam materials to categories
4. All content is automatically organized and displayed

## Production Deployment

Before deploying to production:

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Set up proper database (PostgreSQL recommended)
5. Configure static files serving
6. Set up media files storage
7. Use environment variables for sensitive data

## License

This project is proprietary software for Legal Laboratory.

## Support

For issues or questions, please contact the development team.

