import json
from datetime import datetime

TABLE_FILE = "tables.json"


def load_tables():
    with open(TABLE_FILE, "r") as file:
        return json.load(file)


def save_tables(tables):
    with open(TABLE_FILE, "w") as file:
        json.dump(tables, file, indent=4)


# Step 1: Validate guest count
def validate_guest_count(guests):
    if guests <= 0:
        return False, "Guest count must be greater than 0."

    if guests > 8:
        return False, "Maximum table capacity is 8."

    return True, None


# Step 2: Check whether any table is available
def has_available_tables(tables):
    for table in tables:
        if table["available"]:
            return True
    return False


# Step 3: Find the smallest suitable table (Best Fit)
def find_best_table(tables, guests):
    suitable_tables = []

    for table in tables:
        if table["available"] and table["capacity"] >= guests:
            suitable_tables.append(table)

    if not suitable_tables:
        return None

    suitable_tables.sort(key=lambda t: t["capacity"])

    return suitable_tables[0]


# Step 4: Reserve table
def reserve_table(guests):

    # Validate input
    valid, message = validate_guest_count(guests)

    if not valid:
        return {
            "success": False,
            "message": message
        }

    tables = load_tables()

    # Check availability
    if not has_available_tables(tables):
        return {
            "success": False,
            "message": "No tables are currently available."
        }

    # Find best table
    table = find_best_table(tables, guests)

    if table is None:
        return {
            "success": False,
            "message": "No suitable table found for your group."
        }

    # Reserve table
    table["available"] = False
    save_tables(tables)

    # Generate booking confirmation
    booking_id = f"RES-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "success": True,
        "booking_id": booking_id,
        "table_id": table["table_id"],
        "capacity": table["capacity"],
        "message": "Reservation confirmed."
    }