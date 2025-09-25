# Smart Healthcare Appointment System - Flask + MySQL

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables as needed (optional):

- DB_HOST (default: localhost)
- DB_USER (default: root)
- DB_PASSWORD (default: empty)
- DB_NAME (default: smart_healthcare)
- DB_POOL_SIZE (default: 5)

4. Create database schema:

```bash
mysql -u <user> -p < schema.sql
```

5. Run the server:

```bash
python app.py
```

## Endpoints

- Patients: `GET/POST /patients`, `GET/PUT/DELETE /patients/<id>`
- Doctors: `GET/POST /doctors`, `GET/PUT/DELETE /doctors/<id>`
- Appointments: `GET/POST /appointments`, `GET/PUT/DELETE /appointments/<id>`
- Admins: `GET/POST /admins`, `GET/PUT/DELETE /admins/<id>`
- Availability: `GET/POST /availability`, `GET/PUT/DELETE /availability/<id>`

All responses are JSON with appropriate HTTP status codes. Queries are parameterized to prevent SQL injection. Basic validation and error handling are included.
