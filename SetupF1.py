"""
F1 Telemetry — Load Real 2025 Bahrain GP Data
------------------------------------------------

"""

import requests
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "f1_telemetry"
}

OPENF1_BASE = "https://api.openf1.org/v1"

# sessions 
SESSION_TYPES = ["Practice", "Qualifying", "Race"]
YEAR = 2025
COUNTRY = "Bahrain"


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def wipe_old_data(cursor):
    """Delete everything currently in drivers and laps — clean slate."""
    cursor.execute("DELETE FROM laps")
    cursor.execute("DELETE FROM drivers")
    print("Wiped old sample data from drivers and laps.")


def fetch_sessions():
    """
    Ask OpenF1: 'what sessions happened at the 2025 Bahrain GP?'
    Returns a list of session dictionaries (one per Practice/Qualifying/Race).
    """
    params = {"year": YEAR, "country_name": COUNTRY}
    response = requests.get(f"{OPENF1_BASE}/sessions", params=params)
    response.raise_for_status()  # crashes loudly if the request failed
    sessions = response.json()

    # Keep only the session types we actually want
    relevant = [s for s in sessions if any(t in s["session_type"] for t in SESSION_TYPES)]
    print(f"Found {len(relevant)} relevant sessions for {COUNTRY} {YEAR}.")
    return relevant


def fetch_drivers_for_session(session_key):
    """Ask OpenF1: 'who drove in this specific session?'"""
    params = {"session_key": session_key}
    response = requests.get(f"{OPENF1_BASE}/drivers", params=params)
    response.raise_for_status()
    return response.json()


def fetch_laps_for_session(session_key):
    """Ask OpenF1: 'what laps were driven in this specific session?'"""
    params = {"session_key": session_key}
    response = requests.get(f"{OPENF1_BASE}/laps", params=params)
    response.raise_for_status()
    return response.json()


def insert_drivers(cursor, drivers_data, season, seen_driver_numbers):
    """
    Insert driver info, but skip any driver_number we've already
    inserted for this season (avoids duplicate rows across sessions,
    since the same drivers appear in Practice, Qualifying, and Race).
    """
    rows_to_insert = []
    for d in drivers_data:
        driver_number = d.get("driver_number")
        if driver_number in seen_driver_numbers:
            continue  # already added this driver for this season

        rows_to_insert.append((
            driver_number,
            season,
            d.get("full_name"),
            d.get("team_name"),
            d.get("country_code")  # closest available field to "nationality"
        ))
        seen_driver_numbers.add(driver_number)

    if rows_to_insert:
        cursor.executemany("""
            INSERT INTO drivers (driver_number, season, driver_name, team, nationality)
            VALUES (%s, %s, %s, %s, %s)
        """, rows_to_insert)
        print(f"  Inserted {len(rows_to_insert)} new drivers.")


def insert_laps(cursor, laps_data, season, session_type):
    """Insert lap records, only keeping the columns our table actually has."""
    rows_to_insert = []
    for lap in laps_data:
        lap_duration = lap.get("lap_duration")
        if lap_duration is None:
            continue  # skip incomplete laps (e.g. in/out laps with no time)

        rows_to_insert.append((
            lap.get("driver_number"),
            season,
            lap.get("lap_number"),
            lap_duration,
            session_type
        ))

    if rows_to_insert:
        cursor.executemany("""
            INSERT INTO laps (driver_number, season, lap_number, lap_duration, session_type)
            VALUES (%s, %s, %s, %s, %s)
        """, rows_to_insert)
        print(f"  Inserted {len(rows_to_insert)} laps for {session_type}.")


def main():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        wipe_old_data(cursor)
        conn.commit()

        sessions = fetch_sessions()
        seen_driver_numbers = set()

        for session in sessions:
            session_key = session["session_key"]
            session_type = session["session_type"]  # e.g. "Race", "Qualifying", "Practice"
            print(f"\nProcessing {session_type} (session_key={session_key})...")

            drivers_data = fetch_drivers_for_session(session_key)
            insert_drivers(cursor, drivers_data, YEAR, seen_driver_numbers)

            laps_data = fetch_laps_for_session(session_key)
            insert_laps(cursor, laps_data, YEAR, session_type)

            conn.commit()  # save progress after each session

        print("\nAll done — real 2025 Bahrain GP data loaded.")

    except Error as e:
        print(f"Database error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()