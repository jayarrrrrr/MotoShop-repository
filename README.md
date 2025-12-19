E‑commerce Final Project

## Project Description

This is a Django-based e‑commerce web application implementing a multi-role marketplace with buyers and vendors. Core features include product listings, cart and checkout, order management, user authentication, and a vendor dashboard.

Tech stack: Python, Django, SQLite (development), HTML/CSS/JS, Bootstrap (templates).

## Setup Instructions (Windows)

Prerequisites: Python 3.9+, Git (optional for local work), virtualenv

1. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Apply migrations and create a superuser

```powershell
python manage.py migrate
python manage.py createsuperuser
```

4. (Optional) Load sample data

```powershell
python manage.py loaddata scripts/sample_data.json
```

5. Run the development server

```powershell
python manage.py runserver
```

## Team Members & Roles

- Backend Developer: <NAME> — Database design, authentication, APIs, vendor dashboard
- Frontend Developer: <NAME> — UI/UX, templates, responsive design, buyer pages
- Full‑Stack & DevOps: <NAME> — Integration, repository management, CI/CD, testing

Replace `<NAME>` with actual team member names before submission.

## Features

- User registration, login, password reset
- Product categories, multiple images, and reviews
- Cart and checkout flow
- Order management and order items
- Vendor dashboard: product CRUD and order handling

## Database Schema

See `docs/schema.md` for a summary of models and relationships.

## Contributing & PRs

- Use feature branches and open a Pull Request for review.
- CI runs on push and pull request to `main`.
- Use descriptive commit messages and squash logical changes before merge.

## License

This project is released under the MIT License — see `LICENSE`.
