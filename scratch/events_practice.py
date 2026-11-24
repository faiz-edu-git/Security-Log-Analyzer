from datetime import datetime

events = [
    {
        "raw_line_no": 3,
        "timestamp": datetime(2026, 11, 15, 9, 2, 15),
        "source": "auth-server",
        "event_type": "login_failed",
        "username": "sara",
        "source_ip": "10.0.0.45",
        "message": "Invalid password attempt",
    },
    {
        "raw_line_no": 2,
        "timestamp": datetime(2026, 11, 15, 9, 10, 0),
        "source": "auth-server",
        "event_type": "login_failed",
        "username": "nida",
        "source_ip": "10.0.1.20",
        "message": "Authentication event",},
    {
         "raw_line_no": 1,
        "timestamp": datetime(2026, 11, 15, 9, 18, 0),
        "source": "iam-service",
        "event_type": "privilege_change",
        "username": "admin",
        "source_ip": "192.168.1.5",
        "message": "Account change recorded",
    },
    {
        "raw_line_no": 4,
        "timestamp": datetime(2026, 11, 15, 9, 25, 0),
        "source": "api-gateway",
        "event_type": "data_request",
        "username": "tariq",
        "source_ip": "172.16.0.88",
        "message": "Request received",
    },
    {
        "raw_line_no": 5,
        "timestamp": datetime(2026, 11, 15, 9, 27, 0),
        "source": "auth-server",
        "event_type": "login_failed",
        "username": "kamran",
        "source_ip": "10.0.2.15",
        "message": "Authentication event",
    },
]

for event in events:
    print(event["username"])

for event in events:
    if event["event_type"] == "login failed":
        print(event["message"])

