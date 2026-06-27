
from flask import Flask
from routes.main import main_bp
from routes.api import api_bp


def create_app():
    """Tạo và cấu hình Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'graph-visualizer-secret-key'
    app.config['JSON_AS_ASCII'] = False  # Hỗ trợ tiếng Việt trong JSON

    # Đăng ký Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
