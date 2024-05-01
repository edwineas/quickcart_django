import csv
import json
from datetime import datetime

csvfile = open('auth_user.csv', 'r')
jsonfile = open('auth_user.json', 'w')

fieldnames = ("id","password","last_login","is_superuser","username","last_name","email","is_staff","is_active","date_joined","first_name")
reader = csv.DictReader(csvfile, fieldnames)

# Format the data for Django's loaddata command
data = []
for row in reader:
    if row["id"].isdigit():
        # Check if 'last_login' is in the correct format
        try:
            datetime.strptime(row["last_login"], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            row["last_login"] = None  # Set 'last_login' to None if it's not in the correct format

        data.append({
            "model": "auth.user",
            "pk": int(row["id"]),
            "fields": {key: value for key, value in row.items() if key != "id"}
        })

json.dump(data, jsonfile)