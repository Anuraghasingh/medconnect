from flask import Blueprint, request, jsonify
from mysql.connector import Error as MySQLError

from db import execute_query


patients_bp = Blueprint("patients", __name__)


def _validate_required(fields: list, data: dict):
    missing = [f for f in fields if not data.get(f)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None


@patients_bp.get("")
def list_patients():
    rows = execute_query(
        "SELECT PatientID, Name, Email, Phone, Age, Gender FROM Patient ORDER BY PatientID DESC",
        fetchall=True,
    )
    return jsonify(rows), 200


@patients_bp.post("")
def create_patient():
    data = request.get_json(silent=True) or {}
    required = ["Name", "Email", "Phone", "Password", "Age", "Gender"]
    ok, err = _validate_required(required, data)
    if not ok:
        return jsonify({"error": err}), 400
    try:
        execute_query(
            """
            INSERT INTO Patient (Name, Email, Phone, Password, Age, Gender)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                data["Name"],
                data["Email"],
                data["Phone"],
                data["Password"],
                int(data["Age"]),
                data["Gender"],
            ),
        )
        row = execute_query(
            "SELECT PatientID, Name, Email, Phone, Age, Gender FROM Patient WHERE Email=%s",
            (data["Email"],),
            fetchone=True,
        )
        return jsonify(row), 201
    except MySQLError as e:
        msg = str(e)
        if "1062" in msg:
            return jsonify({"error": "Email already exists"}), 409
        return jsonify({"error": "Database error", "message": msg}), 500


@patients_bp.get("/<int:patient_id>")
def get_patient(patient_id: int):
    row = execute_query(
        "SELECT PatientID, Name, Email, Phone, Age, Gender FROM Patient WHERE PatientID=%s",
        (patient_id,),
        fetchone=True,
    )
    if not row:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(row), 200


@patients_bp.put("/<int:patient_id>")
def update_patient(patient_id: int):
    data = request.get_json(silent=True) or {}
    # Allow partial update except Email uniqueness handled by DB
    allowed_fields = ["Name", "Email", "Phone", "Password", "Age", "Gender"]
    fields = []
    values = []
    for f in allowed_fields:
        if f in data and data[f] is not None:
            fields.append(f"{f}=%s")
            if f == "Age" and data[f] is not None:
                values.append(int(data[f]))
            else:
                values.append(data[f])
    if not fields:
        return jsonify({"error": "No valid fields to update"}), 400
    values.append(patient_id)
    try:
        execute_query(
            f"UPDATE Patient SET {', '.join(fields)} WHERE PatientID=%s",
            tuple(values),
        )
        updated = execute_query(
            "SELECT PatientID, Name, Email, Phone, Age, Gender FROM Patient WHERE PatientID=%s",
            (patient_id,),
            fetchone=True,
        )
        if not updated:
            return jsonify({"error": "Patient not found"}), 404
        return jsonify(updated), 200
    except MySQLError as e:
        msg = str(e)
        if "1062" in msg:
            return jsonify({"error": "Email already exists"}), 409
        return jsonify({"error": "Database error", "message": msg}), 500


@patients_bp.delete("/<int:patient_id>")
def delete_patient(patient_id: int):
    execute_query("DELETE FROM Patient WHERE PatientID=%s", (patient_id,))
    return jsonify({"message": "Deleted"}), 200


