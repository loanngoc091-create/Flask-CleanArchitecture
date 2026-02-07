from flask import Flask
from src.config import Config
from src.api.controllers.auth_controller import bp as auth_bp
from src.api.controllers.syllabus_controller import bp as syllabus_bp
print("🔥🔥🔥 FILE NÀY ĐANG ĐƯỢC CHẠY 🔥🔥🔥")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(syllabus_bp, url_prefix="/syllabus")

    print("===== ROUTES =====")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=9999, debug=True)
