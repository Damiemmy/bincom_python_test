# Bincom Python Assessment

## Overview

A Python solution to the Bincom Python Developer assessment, covering colour-frequency analysis, statistical calculations, PostgreSQL persistence, recursive searching, binary-to-decimal conversion, and Fibonacci sequence calculations.

## Features

- Extracts colour observations from the supplied HTML data.
- Calculates colour frequencies, mean frequency, most-worn colour, median frequency, and population variance.
- Calculates the probability of selecting red.
- Stores colour frequencies in a PostgreSQL database.
- Implements recursive search for a target number.
- Generates a random four-bit binary number and converts it to decimal.
- Calculates the sum of the first 50 Fibonacci numbers.

## Requirements

- Python 3
- PostgreSQL
- Python packages listed in `requirements.txt`

## Setup

### 1. Clone the repository

```bash
git https://github.com/Damiemmy/bincom_python_test.git
cd bincom_python_test
```

Replace the repository URL and folder name with your actual GitHub repository details.

### 2. Create and activate a virtual environment

**Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

For Windows Command Prompt:

```cmd
copy .env.example .env
```

For Linux/macOS Terminal:

cp .env.example .env

Open `.env` and configure your local PostgreSQL credentials:

```dotenv
PGHOST=localhost
PGPORT=5432
PGDATABASE=bincom
PGUSER=bin_user
PGPASSWORD=your_actual_password
```

Replace `your_actual_password` with the password configured for your PostgreSQL user.

### 5. Configure PostgreSQL

Ensure PostgreSQL is installed, running, and accessible from the environment where you run Python.

Connect to PostgreSQL as an administrator and create the database user and database:

```sql
CREATE USER bin_user WITH PASSWORD 'your_actual_password';
CREATE DATABASE bincom OWNER bin_user;
```

Use the same password in your `.env` file.

If the user or database already exists, reuse the existing configuration or update it as necessary. The database user must have permission to create and write to the application's table.

**Note:** If PostgreSQL runs inside WSL while Python runs on Windows, ensure Windows can reach the PostgreSQL server through the configured host and port.

## Running the Application

With your virtual environment activated and `.env` configured, run:

```bash
python bincom_python_test.py
```

The program performs the assessment calculations and attempts to save the colour frequencies to PostgreSQL using the configured credentials.

If the database connection fails, verify that PostgreSQL is running, the database exists, and your host, port, username, and password are correct.

## Database

The application stores colour names and their frequencies in a PostgreSQL table named `colour_frequencies`.

The database table is created by the application when the database connection succeeds. The configured database must already exist, and the database user must have the required permissions.

## Security

- Database credentials are loaded through environment variables.
- The `.env` file contains local credentials and must never be committed to version control.
- The `.env.example` file should contain placeholder values only.
- The `.gitignore` file should exclude `.env`, virtual environments, and Python cache files.

Example `.gitignore`:

```gitignore
.env
venv/
.venv/
__pycache__/
*.py[cod]
```

## Notes

- The supplied colour labels are preserved as provided in the assessment data, including `ARSH` and `BLEW`.
- Statistical calculations operate on the recorded colour frequencies.
- The PostgreSQL persistence feature requires a working database connection.
- Dependencies can be installed using `requirements.txt`.

## Author

Submitted as part of the Bincom Python Developer assessment.
