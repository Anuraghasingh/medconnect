from flask import Blueprint, request, jsonify
from mysql.connector import Error as MySQLError

from db import execute_query


admins_bp = Blueprint("admins", __name__)


def _validate_required(fields: list, data: dict):
    missing = [f for f in fields if not data.get(f)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None


@admins_bp.get("")
def list_admins():
    rows = execute_query(
        "SELECT AdminID, Name, Email FROM Admin ORDER BY AdminID DESC",
        fetchall=True,
    )
    return jsonify(rows), 200


@admins_bp.post("")
def create_admin():
    data = request.get_json(silent=True) or {}
    required = ["Name", "Email", "Password"]
    ok, err = _validate_required(required, data)
    if not ok:
        return jsonify({"error": err}), 400
    try:
        execute_query(
            "INSERT INTO Admin (Name, Email, Password) VALUES (%s, %s, %s)",
            (
                data["Name"],
                data["Email"],
                data["Password"],
            ),
        )
        row = execute_query(
            "SELECT AdminID, Name, Email FROM Admin WHERE Email=%s",
            (data["Email"],),
            fetchone=True,
        )
        return jsonify(row), 201
    except MySQLError as e:
        msg = str(e)
        if "1062" in msg:
            return jsonify({"error": "Email already exists"}), 409
        return jsonify({"error": "Database error", "message": msg}), 500


@admins_bp.get("/<int:admin_id>")
def get_admin(admin_id: int):
    row = execute_query(
        "SELECT AdminID, Name, Email FROM Admin WHERE AdminID=%s",
        (admin_id,),
        fetchone=True,
    )
    if not row:
        return jsonify({"error": "Admin not found"}), 404
    return jsonify(row), 200


@admins_bp.put("/<int:admin_id>")
def update_admin(admin_id: int):
    data = request.get_json(silent=True) or {}
    allowed_fields = ["Name", "Email", "Password"]
    fields = []
    values = []
    for f in allowed_fields:
        if f in data and data[f] is not None:
            fields.append(f"{f}=%s")
            values.append(data[f])
    if not fields:
        return jsonify({"error": "No valid fields to update"}), 400
    values.append(admin_id)
    try:
        execute_query(
            f"UPDATE Admin SET {', '.join(fields)} WHERE AdminID=%s",
            tuple(values),
        )
        updated = execute_query(
            "SELECT AdminID, Name, Email FROM Admin WHERE AdminID=%s",
            (admin_id,),
            fetchone=True,
        )
        if not updated:
            return jsonify({"error": "Admin not found"}), 404
        return jsonify(updated), 200
    except MySQLError as e:
        msg = str(e)
        if "1062" in msg:
            return jsonify({"error": "Email already exists"}), 409
        return jsonify({"error": "Database error", "message": msg}), 500


@admins_bp.delete("/<int:admin_id>")
def delete_admin(admin_id: int):
    execute_query("DELETE FROM Admin WHERE AdminID=%s", (admin_id,))
    return jsonify({"message": "Deleted"}), 200


