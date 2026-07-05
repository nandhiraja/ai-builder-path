TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": (
                "Check which tables are available for a given party size, date, and time slot. "
                "Call this as soon as you know the party size, date, and slot. "
                "A table can be booked for multiple slots on the same day by different customers."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "guests": {
                        "type": "integer",
                        "description": "Number of guests in the party."
                    },
                    "date": {
                        "type": "string",
                        "description": "Reservation date in YYYY-MM-DD format. Must not be in the past."
                    },
                    "slot": {
                        "type": "string",
                        "enum": ["lunch", "afternoon", "dinner"],
                        "description": "Time slot: lunch (12:00-15:00), afternoon (15:00-18:00), dinner (18:00-22:00)."
                    },
                    "location": {
                        "type": "string",
                        "enum": ["indoor", "outdoor"],
                        "description": "Preferred seating area. Include only if the customer specifies."
                    }
                },
                "required": ["guests", "date", "slot"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reserve_table",
            "description": (
                "Reserve a specific table for a customer on a given date and slot. "
                "Only call this after you have: table_id, customer name, date, slot, and exact time. "
                "Never call with missing or placeholder values."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "table_id": {
                        "type": "integer",
                        "description": "Table ID obtained from check_availability or suggest_tables."
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "Customer's full name."
                    },
                    "date": {
                        "type": "string",
                        "description": "Reservation date in YYYY-MM-DD format."
                    },
                    "slot": {
                        "type": "string",
                        "enum": ["lunch", "afternoon", "dinner"],
                        "description": "Time slot being reserved."
                    },
                    "time": {
                        "type": "string",
                        "description": "Exact preferred time within the slot in HH:MM format."
                    }
                },
                "required": ["table_id", "customer_name", "date", "slot", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_tables",
            "description": (
                "Suggest available tables when the customer is unsure which to pick, "
                "or when check_availability returns nothing. Returns tables sorted by best fit."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "guests": {
                        "type": "integer",
                        "description": "Number of guests."
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format."
                    },
                    "slot": {
                        "type": "string",
                        "enum": ["lunch", "afternoon", "dinner"],
                        "description": "Time slot."
                    }
                },
                "required": ["guests", "date", "slot"]
            }
        }
    }
]