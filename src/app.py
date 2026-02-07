from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_cors import CORS
from config import Config
from api.controllers.auth_controller import bp as auth_bp
from api.controllers.syllabus_controller import bp as syllabus_bp
from infrastructure.databases import init_db
from infrastructure.databases.mssql import init_mssql
from flask import send_from_directory
from api.controllers.Hod_controller import bp as review_bp
from infrastructure.databases.db import db
from api.controllers.academic_verification_controller import bp as academic_verify_bp
from api.controllers.principal_controller import bp as principal_bp
from api.controllers.publish_controller import bp as publish_bp
from api.controllers.student_controller import bp as student_bp


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Nhập: Bearer <JWT_TOKEN>"
        }
    }
}

swagger_template = {
    "security": [
        {"BearerAuth": []}
    ]
}

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
    app,
    origins=["http://localhost:5500"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            return "", 200

    Swagger(app, config=swagger_config, template=swagger_template)
    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(syllabus_bp, url_prefix="/syllabus")
    app.register_blueprint(review_bp, url_prefix="/syllabus")
    app.register_blueprint( academic_verify_bp, url_prefix="/syllabus")
    app.register_blueprint(principal_bp, url_prefix="/principal")
    app.register_blueprint(publish_bp, url_prefix="/api")
    app.register_blueprint(student_bp)
    # Database
    init_mssql()
    init_db()
    db.init_app(app) 

    @app.route("/test")
    def test_api():
        return jsonify({
            "status": "OK",
            "message": "API is running"
        })
    
    @app.route("/uploads/<path:filename>")
    def uploaded_files(filename):
        return send_from_directory("uploads", filename)

    print("===== ROUTES =====")
    for r in app.url_map.iter_rules():
        print(r)


    return app
    

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=9999, debug=True)




