# Flourish Demo

## Project Structure

This repository uses a modular folder architecture to keep the code clean, scalable, and easy to navigate. Here is a breakdown of where everything lives:

```text
├── app/                    # The main application code lives here
│   ├── __pycache__/        # Compiled Python files (automatically generated, do not edit)
│   ├── config/             # Configuration settings and database connection setup
│   ├── models/             # SQLAlchemy database models (how data is stored in SQLite)
│   ├── routers/            # API endpoints grouped by module (MarketFresh, Londola, etc.)
│   ├── schemas/            # Pydantic models for data validation and API responses
│   ├── services/           # Core business logic and external integrations
│   └── main.py             # The entry point that initializes the FastAPI application
├── .gitignore              # Specifies which files/folders Git should ignore
├── demo.db                 # Your local SQLite database file
├── poetry.lock             # Locks exact dependency versions for consistent environments
└── pyproject.toml          # The configuration file for Poetry containing project dependencies
```

## Directory Breakdown

- **`app/config/`**: Holds the core configuration settings for the app. This is typically where you define environment variables and configure your SQLite database connection engine.
- **`app/models/`**: The home for your **Data Modeling**. Contains SQLAlchemy classes that define the exact structure, columns, and relationships of your SQL database tables (e.g., `listings` and `transactions`).
- **`app/routers/`**: The home for your **API Design**. Each file here (like `listings.py` or `transactions.py`) defines the API endpoints (`GET`, `POST`, `PUT`, `DELETE`) and acts as the traffic controller, routing requests to the database.
- **`app/schemas/`**: Contains Pydantic classes. These act as the security guards of your API. They validate incoming JSON data from a user to ensure it is correct before it hits the database, and they format the outgoing data before sending it back.
- **`app/services/`**: Holds the heavy lifting and core business logic. If an endpoint requires complex calculations, specific AI functions, or external API calls (like mobile money integrations), that logic is written here to keep the `routers` clean and easy to read.
- **`app/main.py`**: The spark that starts the engine. It brings all the routers together and launches the FastAPI server.

---

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Python (3.10 or newer):** [Download Python here](https://www.python.org/downloads/)
- **Git:** [Download Git here](https://git-scm.com/downloads)
- An IDE like **VS Code** or **PyCharm**.

---

## Setup Instructions

### 1. Clone the Repository

Open your terminal (Mac/Linux) or Command Prompt/PowerShell (Windows) and run:

```bash
git clone https://github.com/stede-technologies/vc-backend.git
cd vc-backend
```

## 2. Install Poetry (Dependency Manager)

We use **Poetry** to manage Python packages and virtual environments.

### For Windows

Open **PowerShell as Administrator** and run:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

> Note: You may need to add the Poetry path to your System Environment Variables.

### For Mac/Linux

Open your terminal and run:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Alternative for Both OS

If you have Python installed, you can simply run:

```bash
pip install poetry
```

### 3. Install Project Dependencies

Once Poetry is installed, initialize the project and install the required packages such as FastAPI, SQLAlchemy, and Uvicorn:

```bash
poetry install
```

### 4. Run the Development Server

Start your FastAPI server with hot-reloading enabled:

```bash
poetry run uvicorn app.main:app --reload
```

You should see a message indicating that the server is running.

- View the app: http://127.0.0.1:8000/
- View the interactive API docs: http://127.0.0.1:8000/docs

This is where you will test your API endpoints!

---

## The Post-Hackathon Challenge

Your goal is to complete the backend logic for the MarketFresh (Listings) and Londola (Transactions) modules.

You must connect the API endpoints to the SQLite database so that data is permanently saved and retrieved.

### Task 1: MarketFresh (Listings)

Navigate to `app/routers/listings.py`.

The endpoints are currently returning dummy data. You need to implement real database operations:

- `POST /api/listings`: Create a new listing and save it to the database.
- `GET /api/listings`: Retrieve a list of all active listings from the database.
- `GET /api/listings/{listing_id}`: Fetch a specific listing by its ID.
- `PUT /api/listings/{listing_id}`: Update an existing listing's details.
- `DELETE /api/listings/{listing_id}`: Delete a listing from the database.

### Task 2: Londola (Transactions)

Navigate to `app/routers/transactions.py`.

Implement the following:

- `POST /api/transactions`: Log a new sale or expense.
- `GET /api/transactions`: Fetch all transactions.
- `GET /api/transactions/{transaction_id}`: Fetch a specific transaction.
- `PUT /api/transactions/{transaction_id}`: Edit a transaction.
- `DELETE /api/transactions/{transaction_id}`: Delete a transaction.
- Bonus challenge: enforce a 24-hour editing window.

---

## How to Succeed: The API + Data Connection

To make these routes work, you must understand how three files communicate:

1. **`app/models.py`**
   - This is your database schema.
   - It defines how the SQLite tables are created using SQLAlchemy.

2. **`app/schemas.py`**
   - This is your API data validator.
   - It uses Pydantic to ensure incoming requests have the correct data (for example, `price` is a number) and formats outgoing responses.

3. **`app/routers/*.py`**
   - This is the controller.
   - It receives the request, validates it using the Pydantic schema, talks to the SQLAlchemy model, saves or fetches data from the database, and returns the response.

---

## Helpful Tips

- Always inject the database session into your routes using:

```python
db: Session = Depends(get_db)
```

- Look at the interactive Swagger documentation (`/docs`) frequently to test your endpoints as you build them.
- Check your terminal for errors! If Pydantic complains, your schemas and models might not be matching up.

Good luck!

Happy coding! 
