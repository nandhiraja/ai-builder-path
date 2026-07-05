import json

DATA_FILE = "restaurant.json"

# Time slot definitions
SLOTS = {
    "lunch":     (12 * 60, 15 * 60),   # 12:00 – 15:00
    "afternoon": (15 * 60, 18 * 60),   # 15:00 – 18:00
    "dinner":    (18 * 60, 22 * 60),   # 18:00 – 22:00
}


def load_tables() -> list:
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tables(tables: list) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(tables, f, indent=4)


def _is_booked(table: dict, date: str, slot: str) -> bool:
    """Return True if the table already has a booking for this date + slot."""
    return any(
        b["date"] == date and b["slot"] == slot
        for b in table.get("bookings", [])
    )


def check_availability(guests: int, date: str, slot: str, location: str = None) -> dict:
    """
    Return available tables for the given party size, date, and time slot.
    A table is available if it has no booking for that date + slot.
    """
    tables = load_tables()
    results = [
        {
            "table_id": t["table_id"],
            "label": t["label"],
            "capacity": t["capacity"],
            "location": t["location"]
        }
        for t in tables
        if t["capacity"] >= guests
        and not _is_booked(t, date, slot)
        and (location is None or t["location"] == location)
    ]

    if results:
        return {"found": True, "tables": results}
    return {
        "found": False,
        "tables": [],
        "message": f"No tables available for {guests} guests during {slot} on {date}."
    }


def reserve_table(table_id: int, customer_name: str, date: str, slot: str, time: str) -> dict:
    """
    Reserve a table for a specific date and slot.
    The same table can be booked by different people across different slots / dates.
    """
    tables = load_tables()

    for table in tables:
        if table["table_id"] != table_id:
            continue

        if _is_booked(table, date, slot):
            return {
                "success": False,
                "message": f"Table {table['label']} is already booked for {slot} on {date}. Please choose another slot or table."
            }

        table["bookings"].append({
            "date": date,
            "slot": slot,
            "booked_by": customer_name,
            "booked_time": time
        })
        save_tables(tables)

        return {
            "success": True,
            "booking_id": f"RES-{table_id}-{date.replace('-', '')}-{slot}",
            "customer_name": customer_name,
            "table_id": table_id,
            "table_label": table["label"],
            "location": table["location"],
            "date": date,
            "slot": slot,
            "time": time,
            "message": f"Confirmed! {table['label']} reserved for {customer_name} — {slot} on {date} at {time}."
        }

    return {"success": False, "message": f"Table {table_id} not found."}


def suggest_tables(guests: int, date: str, slot: str) -> dict:
    """
    Suggest available tables sorted by best fit for the party size.
    """
    tables = load_tables()
    suggestions = sorted(
        [
            {
                "table_id": t["table_id"],
                "label": t["label"],
                "capacity": t["capacity"],
                "location": t["location"]
            }
            for t in tables
            if t["capacity"] >= guests and not _is_booked(t, date, slot)
        ],
        key=lambda t: t["capacity"]
    )

    if suggestions:
        return {"found": True, "suggestions": suggestions}
    return {
        "found": False,
        "suggestions": [],
        "message": f"No tables available for {slot} on {date}."
    }