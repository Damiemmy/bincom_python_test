# Bincom Python Assessment

## Overview

A Python solution to the Bincom Python Developer assessment, covering colour-frequency analysis, statistical calculations, PostgreSQL persistence, recursive searching, binary-to-decimal conversion, and Fibonacci sequence calculations.

## Features

- Extracts colour observations from the supplied HTML data.
- Calculates colour frequencies, mean frequency, most-worn colour, median frequency, and population variance.
- Calculates the probability of selecting red.
- Stores colour frequencies in PostgreSQL.
- Implements recursive search for a target number.
- Generates a random four-digit binary number and converts it to decimal.
- Calculates the sum of the first 50 Fibonacci numbers.

## Requirements

- Python 3
- PostgreSQL
- Python packages listed in `requirements.txt`

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a local `.env` file using `.env.example` as a template.
5. Configure your PostgreSQL database and credentials in `.env`.
6. Run the assessment:

   ```bash
   python bincom_python_test.py
   ```

## Database

The application uses PostgreSQL to store colour names and their frequencies. Ensure the configured database exists and the database user has permission to create and write to the required table.

## Security

Database credentials are provided through environment variables. The `.env` file is excluded from version control and should never be committed.

## Notes

The supplied colour labels are preserved as provided in the assessment data. Statistical calculations operate on the recorded colour frequencies.

