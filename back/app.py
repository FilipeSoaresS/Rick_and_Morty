from flask import Flask, jsonify
from src.models import db
from config.settings import DATABASE_URI
from src.routes.student_routes import students_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

app.register_blueprint(students_bp, url_prefix='/students')

if __name__ == "__main__":
    app.run(debug=True),