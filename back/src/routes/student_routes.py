from flask import Blueprint, jsonify
from src.controllers.students_controller import StudentController

students_bp = Blueprint('students_bp', __name__)
students_controller = StudentController()

@students_bp.route('/', methods=['GET'])
def get_students():
    return students_controller.get_student()