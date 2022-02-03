from app import app
from app.classes import figures, chessboard
from flask import jsonify, abort
import app.classes as classes


@app.route("/api/v1/<chess_figure>/<current_field>", methods=["GET"])
def available_moves(chess_figure: str, current_field: str):
    if chess_figure.capitalize() not in figures:
        response = {
            "availableMoves": [],
            "error": "Figure does not exist.",
            "figure": chess_figure,
            "currentField": current_field,
        }
        abort(404, response)

    if current_field.upper() not in chessboard.values():
        response = {
            "availableMoves": [],
            "error": "Field does not exist.",
            "figure": chess_figure,
            "currentField": current_field,
        }
        abort(409, response)

    my_class = getattr(classes, chess_figure.capitalize())
    obj = my_class(current_field.upper(), chess_figure.capitalize())
    method_to_call = getattr(obj, "list_available_moves")
    available_moves = method_to_call()

    response = {
        "availableMoves": available_moves,
        "error": None,
        "figure": chess_figure,
        "currentField": current_field,
    }

    return jsonify(response), 200


@app.route("/api/v1/<chess_figure>/<current_field>/<dest_field>", methods=["GET"])
def validate_move(chess_figure: str, current_field: str, dest_field: str):
    if chess_figure.capitalize() not in figures:
        response = {
            "move": "invalid",
            "figure": chess_figure,
            "error": "Figure does not exist.",
            "currentField": current_field,
            "destField": dest_field,
        }
        abort(404, response)

    if (
        current_field.upper() not in chessboard.values()
        or dest_field.upper() not in chessboard.values()
    ):
        response = {
            "move": "invalid",
            "figure": chess_figure,
            "error": "Field does not exist.",
            "currentField": current_field,
            "destField": dest_field,
        }
        abort(409, response)

    my_class = getattr(classes, chess_figure.capitalize())
    obj = my_class(current_field.upper(), chess_figure.capitalize())
    method_to_call = getattr(obj, "validate_move")
    valid = method_to_call(dest_field.upper())

    if valid:
        response = {
            "move": "valid",
            "figure": chess_figure,
            "error": None,
            "currentField": current_field,
            "destField": dest_field,
        }
    else:
        response = {
            "move": "invalid",
            "figure": chess_figure,
            "error": "Current move is not permitted.",
            "currentField": current_field,
            "destField": dest_field,
        }

    return jsonify(response), 200


@app.errorhandler(404)
def custom404(e):
    response = jsonify(e.description)
    return response, 404


@app.errorhandler(409)
def custom409(e):
    response = jsonify(e.description)
    return response, 409


@app.errorhandler(500)
def custom500(e):
    return "Internal server error", 500
