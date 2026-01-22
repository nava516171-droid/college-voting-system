# College Voting System - Backend

A comprehensive backend API for a college voting system built with FastAPI and PostgreSQL.

## Features

- **User Authentication**: Register and login with JWT tokens
- **Role-Based Access Control**: Admin, Election Officer, and Student roles
- **Election Management**: Create, update, and manage elections
- **Candidate Management**: Add candidates to elections
- **Voting System**: Cast votes and prevent duplicate voting
- **Results**: View voting results and statistics

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **Validation**: Pydantic

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip

## Installation

1. **Clone the repository**
   ```bash
   cd college voting system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` with your PostgreSQL credentials:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/college_voting_db
   SECRET_KEY=your-secret-key-here
   ```

5. **Create PostgreSQL database**
   ```bash
   createdb college_voting_db
   ```

## Running the Application

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Project Structure

```
college voting system/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── routes/          # API endpoints
│   ├── schemas/         # Pydantic schemas
│   ├── utils/           # Utility functions (security, etc.)
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── __init__.py
├── tests/               # Test files
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

### Elections
- `POST /api/elections/` - Create election (Admin/Officer only)
- `GET /api/elections/` - Get all elections
- `GET /api/elections/{election_id}` - Get election details
- `PUT /api/elections/{election_id}` - Update election
- `DELETE /api/elections/{election_id}` - Delete election

### Candidates
- `POST /api/candidates/` - Create candidate (Admin/Officer only)
- `GET /api/candidates/election/{election_id}` - Get candidates for election
- `GET /api/candidates/{candidate_id}` - Get candidate details
- `PUT /api/candidates/{candidate_id}` - Update candidate
- `DELETE /api/candidates/{candidate_id}` - Delete candidate

### Votes
- `POST /api/votes/` - Cast a vote
- `GET /api/votes/election/{election_id}` - Get election results
- `GET /api/votes/user/{election_id}` - Check if user voted

## Database Schema

### Users
- id, roll_number, email, full_name, hashed_password, role, is_active, created_at, updated_at

### Elections
- id, title, description, status, start_time, end_time, is_active, created_at, updated_at

### Candidates
- id, election_id, name, description, symbol_number, created_at

### Votes
- id, user_id, election_id, candidate_id, created_at (with unique constraint on user_id + election_id)

## Testing

Run tests using pytest:

```bash
pytest tests/
```

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- Role-based access control
- One vote per user per election
- Database constraints for data integrity

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Secret key for JWT encoding
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `DEBUG` - Debug mode

## Contributing

1. Create a feature branch
2. Commit changes
3. Push to the branch
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please contact the development team.
