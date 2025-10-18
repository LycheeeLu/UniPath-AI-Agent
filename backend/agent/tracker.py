import datetime

def generate_tracker(user_id):
    tracker = {
        "user_id": user_id,
        "created": str(datetime.date.today()),
        "universities": [
            {"name": "Stanford University", "status": "Not Started"},
            {"name": "MIT", "status": "In Progress"},
            {"name": "Oxford University", "status": "Submitted"}
        ]
    }
    return tracker
