from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from config import AppConfig
from db import init_connection_pool
from flask_cors import CORS

# Blueprints
from routes.patients import patients_bp
from routes.doctors import doctors_bp
from routes.appointments import appointments_bp
from routes.admins import admins_bp
from routes.availability import availability_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    CORS(app)

    # Initialize DB connection pool
    try:
        init_connection_pool(
            host=app.config.get("DB_HOST"),
            user=app.config.get("DB_USER"),
            password=app.config.get("DB_PASSWORD"),
            database=app.config.get("DB_NAME"),
            pool_name=app.config.get("DB_POOL_NAME"),
            pool_size=app.config.get("DB_POOL_SIZE"),
        )
    except Exception as e:
        print(f"Warning: Could not initialize DB pool: {e}")
        print("App will start but DB operations will fail until DB is available.")

    # Register blueprints
    app.register_blueprint(patients_bp, url_prefix="/patients")
    app.register_blueprint(doctors_bp, url_prefix="/doctors")
    app.register_blueprint(appointments_bp, url_prefix="/appointments")
    app.register_blueprint(admins_bp, url_prefix="/admins")
    app.register_blueprint(availability_bp, url_prefix="/availability")

    @app.route("/health", methods=["GET"])
    def health() -> tuple:
        return jsonify({"status": "ok"}), 200

    # Global error handler for JSON errors
    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            response = {"error": error.name, "message": error.description}
            return jsonify(response), error.code
        # Non-HTTP exceptions
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000, debug=True)


