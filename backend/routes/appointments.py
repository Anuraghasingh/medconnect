from flask import Blueprint, request, jsonify

from db import execute_query


appointments_bp = Blueprint("appointments", __name__)


def _validate_required(fields: list, data: dict):
    missing = [f for f in fields if data.get(f) in (None, "")]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None


@appointments_bp.get("")
def list_appointments():
    rows = execute_query(
        """
        SELECT AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentTime, Status
        FROM Appointment ORDER BY AppointmentID DESC
        """,
        fetchall=True,
    )
    return jsonify(rows), 200


@appointments_bp.post("")
def create_appointment():
    data = request.get_json(silent=True) or {}
    required = ["PatientID", "DoctorID", "AppointmentDate", "AppointmentTime", "Status"]
    ok, err = _validate_required(required, data)
    if not ok:
        return jsonify({"error": err}), 400

    # Check FKs
    patient = execute_query("SELECT PatientID FROM Patient WHERE PatientID=%s", (int(data["PatientID"]),), fetchone=True)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    doctor = execute_query("SELECT DoctorID FROM Doctor WHERE DoctorID=%s", (int(data["DoctorID"]),), fetchone=True)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    # Optionally check availability (if exists and marked available)
    availability = execute_query(
        """
        SELECT AvailabilityID FROM DoctorAvailability
        WHERE DoctorID=%s AND Date=%s AND TimeSlot=%s AND IsAvailable=1
        """,
        (int(data["DoctorID"]), data["AppointmentDate"], data["AppointmentTime"]),
        fetchone=True,
    )
    if availability is None:
        # Not blocking, but inform client
        pass

    execute_query(
        """
        INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, AppointmentTime, Status)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            int(data["PatientID"]),
            int(data["DoctorID"]),
            data["AppointmentDate"],
            data["AppointmentTime"],
            data["Status"],
        ),
    )
    row = execute_query(
        "SELECT AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentTime, Status FROM Appointment ORDER BY AppointmentID DESC LIMIT 1",
        fetchone=True,
    )
    return jsonify(row), 201


@appointments_bp.get("/<int:appointment_id>")
def get_appointment(appointment_id: int):
    row = execute_query(
        "SELECT AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentTime, Status FROM Appointment WHERE AppointmentID=%s",
        (appointment_id,),
        fetchone=True,
    )
    if not row:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(row), 200


@appointments_bp.put("/<int:appointment_id>")
def update_appointment(appointment_id: int):
    data = request.get_json(silent=True) or {}
    allowed_fields = ["PatientID", "DoctorID", "AppointmentDate", "AppointmentTime", "Status"]
    fields = []
    values = []
    for f in allowed_fields:
        if f in data and data[f] is not None:
            fields.append(f"{f}=%s")
            if f in ("PatientID", "DoctorID"):
                values.append(int(data[f]))
            else:
                values.append(data[f])
    if not fields:
        return jsonify({"error": "No valid fields to update"}), 400
    values.append(appointment_id)
    execute_query(
        f"UPDATE Appointment SET {', '.join(fields)} WHERE AppointmentID=%s",
        tuple(values),
    )
    updated = execute_query(
        "SELECT AppointmentID, PatientID, DoctorID, AppointmentDate, AppointmentTime, Status FROM Appointment WHERE AppointmentID=%s",
        (appointment_id,),
        fetchone=True,
    )
    if not updated:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(updated), 200


@appointments_bp.delete("/<int:appointment_id>")
def delete_appointment(appointment_id: int):
    execute_query("DELETE FROM Appointment WHERE AppointmentID=%s", (appointment_id,))
    return jsonify({"message": "Deleted"}), 200


