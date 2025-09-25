from flask import Blueprint, request, jsonify

from db import execute_query


availability_bp = Blueprint("availability", __name__)


def _validate_required(fields: list, data: dict):
    missing = [f for f in fields if data.get(f) in (None, "")]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None


@availability_bp.get("")
def list_availability():
    rows = execute_query(
        """
        SELECT AvailabilityID, DoctorID, Date, TimeSlot, IsAvailable
        FROM DoctorAvailability ORDER BY AvailabilityID DESC
        """,
        fetchall=True,
    )
    return jsonify(rows), 200


@availability_bp.post("")
def create_availability():
    data = request.get_json(silent=True) or {}
    required = ["DoctorID", "Date", "TimeSlot", "IsAvailable"]
    ok, err = _validate_required(required, data)
    if not ok:
        return jsonify({"error": err}), 400

    # Ensure doctor exists
    doctor = execute_query(
        "SELECT DoctorID FROM Doctor WHERE DoctorID=%s",
        (int(data["DoctorID"]),),
        fetchone=True,
    )
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    execute_query(
        """
        INSERT INTO DoctorAvailability (DoctorID, Date, TimeSlot, IsAvailable)
        VALUES (%s, %s, %s, %s)
        """,
        (
            int(data["DoctorID"]),
            data["Date"],
            data["TimeSlot"],
            bool(data["IsAvailable"]),
        ),
    )
    row = execute_query(
        "SELECT AvailabilityID, DoctorID, Date, TimeSlot, IsAvailable FROM DoctorAvailability ORDER BY AvailabilityID DESC LIMIT 1",
        fetchone=True,
    )
    return jsonify(row), 201


@availability_bp.get("/<int:availability_id>")
def get_availability(availability_id: int):
    row = execute_query(
        "SELECT AvailabilityID, DoctorID, Date, TimeSlot, IsAvailable FROM DoctorAvailability WHERE AvailabilityID=%s",
        (availability_id,),
        fetchone=True,
    )
    if not row:
        return jsonify({"error": "Availability not found"}), 404
    return jsonify(row), 200


@availability_bp.put("/<int:availability_id>")
def update_availability(availability_id: int):
    data = request.get_json(silent=True) or {}
    allowed_fields = ["DoctorID", "Date", "TimeSlot", "IsAvailable"]
    fields = []
    values = []
    for f in allowed_fields:
        if f in data and data[f] is not None:
            fields.append(f"{f}=%s")
            if f == "DoctorID":
                values.append(int(data[f]))
            elif f == "IsAvailable":
                values.append(bool(data[f]))
            else:
                values.append(data[f])
    if not fields:
        return jsonify({"error": "No valid fields to update"}), 400
    values.append(availability_id)
    execute_query(
        f"UPDATE DoctorAvailability SET {', '.join(fields)} WHERE AvailabilityID=%s",
        tuple(values),
    )
    updated = execute_query(
        "SELECT AvailabilityID, DoctorID, Date, TimeSlot, IsAvailable FROM DoctorAvailability WHERE AvailabilityID=%s",
        (availability_id,),
        fetchone=True,
    )
    if not updated:
        return jsonify({"error": "Availability not found"}), 404
    return jsonify(updated), 200


@availability_bp.delete("/<int:availability_id>")
def delete_availability(availability_id: int):
    execute_query("DELETE FROM DoctorAvailability WHERE AvailabilityID=%s", (availability_id,))
    return jsonify({"message": "Deleted"}), 200


