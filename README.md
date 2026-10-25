# Students Database CRUD API

A backend application to manage student records using **FastAPI** and **SQLite**.
It supports Create, Read, Update and Delete (CRUD) operations, with input validation
and filtering.

## Features

- Add, view, update and delete students
- List all students, or filter by name, course and birth year
- Input validation (valid email, at least one of email/phone, no future birth date)
- Clear errors for missing records (404) and duplicate emails (400)
- Data is stored permanently in a SQLite database file

## Tech Stack

- Python 3.9+
- FastAPI
- SQLite (through SQLAlchemy)
- Pydantic (validation)
- Uvicorn (server)

## Project Structure

```
students-crud/
├── app/
│   ├── __init__.py
│   ├── main.py        # API endpoints
│   ├── database.py    # Database connection
│   ├── models.py      # Student table definition
│   └── schemas.py     # Validation rules
├── requirements.txt
├── README.md
└── .gitignore
```

## Prerequisites

- Python 3.9 or newer
- Git (to clone the project)

## Installation

1. Clone the repository and open the folder:

```bash
git clone https://github.com/rahul-luffy/students-crud.git
cd students-crud
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate it:

```bash
# Windows (Command Prompt / PowerShell)
venv\Scripts\activate

# Windows (Git Bash)
source venv/Scripts/activate

# Mac / Linux
source venv/bin/activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

The server starts at `http://127.0.0.1:8000`.
The database file `students.db` is created automatically on first run.

## API Testing

Open the interactive API page in your browser:

**http://127.0.0.1:8000/docs**

Click an endpoint, then **Try it out**, fill in the values, and click **Execute**.

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/students` | Create a student |
| GET | `/students` | List / filter students |
| GET | `/students/{student_id}` | View one student |
| PATCH | `/students/{student_id}` | Update a student's details |
| DELETE | `/students/{student_id}` | Delete a student |

### Filters for `GET /students`

| Parameter | Example | Meaning |
|-----------|---------|---------|
| `name` | `/students?name=ram` | Name contains "ram" (not case sensitive) |
| `course` | `/students?course=CSE` | Course contains "CSE" |
| `born_after` | `/students?born_after=2005` | Born after the year 2005 |
| `born_before` | `/students?born_before=2002` | Born before the year 2002 |

Filters can be combined, e.g. `/students?course=CSE&born_after=2002`.

## Student Fields

| Field | Required | Notes |
|-------|----------|-------|
| `id` | auto | Unique student ID, created automatically |
| `name` | yes | 2 to 100 characters |
| `date_of_birth` | yes | Format `YYYY-MM-DD`, cannot be in the future |
| `email` | one of email/phone | Must be a valid email, must be unique |
| `phone` | one of email/phone | 7 to 15 characters |
| `course` | no | |
| `address` | no | |
| `enrollment_date` | no | Format `YYYY-MM-DD` |

## Sample Requests

**Create a student** (`POST /students`):

```json
{
  "name": "Sita Sharma",
  "date_of_birth": "2006-03-15",
  "email": "sita@example.com",
  "course": "B.Tech CSE"
}
```

**Update a student** (`PATCH /students/1`), only the fields you send are changed:

```json
{
  "phone": "9811111111",
  "course": "B.Tech AI"
}
```

**Using curl:**

```bash
curl -X POST "http://127.0.0.1:8000/students" \
  -H "Content-Type: application/json" \
  -d '{"name": "Hari Karki", "date_of_birth": "2001-11-02", "phone": "9822222222", "course": "BBA"}'

curl "http://127.0.0.1:8000/students?course=CSE"

curl -X DELETE "http://127.0.0.1:8000/students/1"
```

## Error Responses

| Code | When |
|------|------|
| 201 | Student created |
| 400 | Email already exists |
| 404 | Student not found |
| 422 | Invalid input (e.g. bad email, missing contact, future birth date) |

## Notes

- Only dummy data is used. No real student information is stored in this repository.
- `students.db` is not uploaded to GitHub (it is listed in `.gitignore`).