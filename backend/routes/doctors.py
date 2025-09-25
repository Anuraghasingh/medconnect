from flask import Blueprint, request, jsonify
from mysql.connector import Error as MySQLError

from db import execute_query


doctors_bp = Blueprint("doctors", __name__)


def _validate_required(fields: list, data: dict):
    missing = [f for f in fields if not data.get(f)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None


@doctors_bp.get("")
def list_doctors():
    rows = execute_query(
        "SELECT DoctorID, Name, Email, Phone, Specialty FROM Doctor ORDER BY DoctorID DESC",
        fetchall=True,
    )
    return jsonify(rows), 200


@doctors_bp.post("")
def create_doctor():
    data = request.get_json(silent=True) or {}
    required = ["Name", "Email", "Phone", "Specialty", "Password"]
    ok, err = _validate_required(required, data)
    if not ok:
        return jsonify({"error": err}), 400
    try:
        execute_query(
            """
            INSERT INTO Doctor (Name, Email, Phone, Specialty, Password)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["Name"],
                data["Email"],
                data["Phone"],
                data["Specialty"],
                data["Password"],
            ),
        )
        row = execute_query(
            "SELECT DoctorID, Name, Email, Phone, Specialty FROM Doctor WHERE Email=%s",
            (data["Email"],),
            fetchone=True,
        )
        return jsonify(row), 201
    except MySQLError as e:
        msg = str(e)
        if "1062" in msg:
            return jsonify({"error": "Email already exists"}), 409
        return jsonify({"error": "Database error", "message": msg}), 500


@doctors_bp.get("/<int:doctor_id>")
def get_doctor(doctor_id: int):
    row = execute_query(
        "SELECT DoctorID, Name, Email, Phone, Specialty FROM Doctor WHERE DoctorID=%s",
        (doctor_id,),
        fetchone=True,
    )
    if not row:
        return jsonify({"error": "Doctor not found"}), 404
    return jsonify(row), 200


@doctors_bp.put("/<int:doctor_id>")
def update_doctor(doctor_id: int):
    data = request.get_json(silent=True) or {}
    allowed_fields = ["Name", "Email", "Phone", "Specialty", "Password"]
    fields = []
    values = []
    for f in allowed_fields:
        if f in data and data[f] is not None:
            fields.append(f"{f}=%s")
            values.append(data[f])
    if not fields:
        return jsonify({"error": "No valid fields to update"}), 400
    values.append(doctor_id)
    try:
        execute_query(
            f"UPDATE Doctor SET {', '.join(fields)} WHERE DoctorID=%s",
            tuple(values),
        )
        updated = execute_query(
            "SELECT DoctorID, Name, Email, Phone, Specialty FROM Doctor WHERE DoctorID=%s",
            (doctor_id,),
            fetchone=True,
        )
        if not updated:
            return jsonify({"error": "Doctor not found"}), 404
        return jsonify(updated), 200
    except MySQLError as e:
        msg = str(e)
        if "1062" in msg:
            return jsonify({"error": "Email already exists"}), 409
        return jsonify({"error": "Database error", "message": msg}), 500


@doctors_bp.delete("/<int:doctor_id>")
def delete_doctor(doctor_id: int):
    execute_query("DELETE FROM Doctor WHERE DoctorID=%s", (doctor_id,))
    return jsonify({"message": "Deleted"}), 200


