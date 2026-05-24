**How All Files Connect — The Big Picture**



HTTP Request comes in (Thunder Client / Postman / Frontend)
         ↓
    urls.py 
    "which view handles this URL?"
         ↓
    views.py
    "run the business logic"
    "talk to the database via models"
    "validate data via serializers"
         ↓
    models.py ←→ Database (db.sqlite3)
    "the actual data structure"
    "relationships between tables"
         ↓
    serializers.py
    "convert Python objects to JSON"
         ↓
HTTP Response goes back (JSON data)