from flask import jsonify

class StudentController:

    def get_student(self):
        try:
            return jsonify({
                "student" : "pedro"
                })

        except Exception:
            return jsonify({
                "erro": "aconteceu algum erro"
                }), 500