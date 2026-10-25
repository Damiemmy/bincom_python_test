
"""
Bincom Python Basic Developer Test
Damisa Emmanuel

Run:
    python bincom_python_test.py

Optional PostgreSQL:
    pip install psycopg2-binary

Set these environment variables before running:
    PGDATABASE, PGUSER, PGPASSWORD
    Optional: PGHOST, PGPORT
"""

import os
import re
import random
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()

# The original colour data from Monday to Friday.
# ARSH and BLEW are preserved exactly as provided.

HTML_DATA = """
<table>
<tr><td>MONDAY</td><td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW,
ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td></tr>

<tr><td>TUESDAY</td><td>ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK,
ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE</td></tr>

<tr><td>WEDNESDAY</td><td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW,
ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE</td></tr>

<tr><td>THURSDAY</td><td>BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW,
ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN</td></tr>

<tr><td>FRIDAY</td><td>GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE,
RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE</td></tr>
</table>
"""


def extract_colours(html):
    """Get all the colour names from the HTML table."""
    rows = re.findall(
        r"<tr\b[^>]*>(.*?)</tr>",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    colours = []

    for row in rows:
        cells = re.findall(
            r"<td\b[^>]*>(.*?)</td>",
            row,
            flags=re.IGNORECASE | re.DOTALL
        )

        if len(cells) < 2:
            continue

        day = re.sub(r"<[^>]+>", "", cells[0]).strip().upper()

        if day not in ("MONDAY", "TUESDAY", "WEDNESDAY",
                       "THURSDAY", "FRIDAY"):
            continue

        colour_text = re.sub(r"<[^>]+>", "", cells[1])

        for colour in colour_text.split(","):
            colour = colour.strip().upper()

            if colour:
                colours.append(colour)

    if not colours:
        raise ValueError("No colours were found in the HTML data.")

    return colours


def recursive_search(numbers, target, index=0):
    """Search a list using recursion."""
    if index == len(numbers):
        return False

    if numbers[index] == target:
        return True

    return recursive_search(numbers, target, index + 1)


def binary_to_decimal(binary):
    """Convert a binary string to a decimal number."""
    decimal = 0

    for digit in binary:
        decimal = decimal * 2 + int(digit)

    return decimal


def fibonacci_numbers(n):
    """Generate the first n Fibonacci numbers, starting with 0 and 1."""
    numbers = []
    a, b = 0, 1

    for _ in range(n):
        numbers.append(a)
        a, b = b, a + b

    return numbers


def save_to_postgresql(frequencies):
    """Save colour frequencies to PostgreSQL when credentials are available."""
    database = os.getenv("PGDATABASE")
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")

    if not database or not user or not password:
        print("\nPostgreSQL skipped: database credentials are not set.")
        return

    try:
        import psycopg2

        connection = psycopg2.connect(
            host=os.getenv("PGHOST", "localhost"),
            port=os.getenv("PGPORT", "5432"),
            dbname=database,
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
        )

        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS colour_frequencies (
                        colour VARCHAR(50) PRIMARY KEY,
                        frequency INTEGER NOT NULL
                    )
                """)

                for colour, frequency in frequencies.items():
                    cursor.execute("""
                        INSERT INTO colour_frequencies (colour, frequency)
                        VALUES (%s, %s)
                        ON CONFLICT (colour)
                        DO UPDATE SET frequency = EXCLUDED.frequency
                    """, (colour, frequency))

        connection.close()
        print("Colour frequencies saved to PostgreSQL.")

    except ImportError:
        print("Install the PostgreSQL driver: pip install psycopg2-binary")

    except Exception as error:
        print("PostgreSQL error:", error)


def main():
    # 1. Extract the colours and count each one.
    colours = extract_colours(HTML_DATA)
    frequencies = Counter(colours)
    total = len(colours)

    print("BINCOM STAFF DRESS COLOUR ANALYSIS")
    print("=" * 36)
    print("Total colour observations:", total)

    print("\nColour frequencies:")
    for colour, count in sorted(frequencies.items()):
        print(f"{colour}: {count}")

    # 2. Mean and variance of the frequencies.
    counts = list(frequencies.values())
    mean = sum(counts) / len(counts)

    variance = sum((count - mean) ** 2 for count in counts) / len(counts)

    # A colour name has no numerical mean.
    # This finds the colour(s) whose frequency is closest to the mean.
    closest_colours = [
        colour for colour, count in frequencies.items()
        if abs(count - mean) == min(abs(value - mean) for value in counts)
    ]

    print("\nMean frequency:", round(mean, 2))
    print("Colour(s) nearest to mean frequency:",
          ", ".join(sorted(closest_colours)))

    # 3. Find the most frequently worn colour.
    highest_count = max(counts)

    most_worn = [
        colour for colour, count in frequencies.items()
        if count == highest_count
    ]

    print("Most-worn colour:", ", ".join(sorted(most_worn)))
    print("Number of times worn:", highest_count)

    # 4. Find the median of the frequencies.
    sorted_counts = sorted(counts)
    middle = len(sorted_counts) // 2

    if len(sorted_counts) % 2 == 1:
        median = sorted_counts[middle]
    else:
        median = (sorted_counts[middle - 1] + sorted_counts[middle]) / 2

    print("Median frequency:", median)

    # The median is a frequency, not a colour name.
    median_colours = [
        colour for colour, count in frequencies.items()
        if count == median
    ]

    if median_colours:
        print("Colour(s) with the median frequency:",
              ", ".join(sorted(median_colours)))
    else:
        print("No single colour has exactly the median frequency.")

    print("Population variance:", round(variance, 4))

    # 5. Probability of randomly selecting RED.
    red_count = frequencies.get("RED", 0)
    probability = red_count / total

    print(f"Probability of RED: {red_count}/{total} = {probability:.4f}")

    # 6. Save the results to PostgreSQL if configured.
    save_to_postgresql(frequencies)

    # 7. Demonstrate recursive search.
    numbers = [3, 8, 12, 19, 25, 31]

    try:
        target = int(input("\nEnter a number to search for: "))

        if recursive_search(numbers, target):
            print("Number found.")
        else:
            print("Number not found.")

        print("List:", numbers)

    except ValueError:
        print("Please enter a valid integer.")

    # 8. Generate a random 4-bit binary number.
    binary = "".join(random.choice("01") for _ in range(4))

    print("\nRandom binary number:", binary)
    print("Decimal equivalent:", binary_to_decimal(binary))

    # 9. Generate and sum the first 50 Fibonacci numbers.
    fibonacci = fibonacci_numbers(50)

    print("\nSum of the first 50 Fibonacci numbers:",
          sum(fibonacci))


if __name__ == "__main__":
    main()
